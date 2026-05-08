import customtkinter as ctk
from tkinter import filedialog, messagebox
import lxml.etree as ET
import os
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT     = "#4a90e2"
ACCENT_HOV = "#357abd"
BG_CARD    = "#1e2130"
BG_INPUT   = "#252839"
TEXT_MAIN  = "#e8eaf6"
TEXT_DIM   = "#7986a8"
GREEN      = "#4caf82"
RED        = "#e05c6a"
AMBER      = "#f5a623"


class FileRow(ctk.CTkFrame):
    """Compact row: icon + label + entry + browse button."""

    def __init__(self, parent, icon: str, label: str, filetypes: list, save: bool = False, **kwargs):
        super().__init__(parent, fg_color=BG_CARD, corner_radius=10, **kwargs)
        self._filetypes = filetypes
        self._save = save

        self.path_var = ctk.StringVar()

        # ── Top label ─────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            header,
            text=f"{icon}  {label}",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color=TEXT_DIM,
            anchor="w",
        ).pack(side="left")

        # ── Entry + button row ─────────────────────────────────────────
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 12))

        self.entry = ctk.CTkEntry(
            row,
            textvariable=self.path_var,
            font=ctk.CTkFont("Segoe UI", 12),
            fg_color=BG_INPUT,
            border_color="#2e3250",
            text_color=TEXT_MAIN,
            placeholder_text="No file selected…",
            placeholder_text_color=TEXT_DIM,
            height=36,
            corner_radius=8,
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            row,
            text="Browse",
            font=ctk.CTkFont("Segoe UI", 12),
            width=100,
            height=36,
            corner_radius=8,
            fg_color="#2a2d40",
            hover_color="#353857",
            text_color=TEXT_MAIN,
            command=self._pick,
        ).pack(side="right")

    def _pick(self):
        if self._save:
            path = filedialog.asksaveasfilename(
                title="Save output as",
                defaultextension=".html",
                filetypes=self._filetypes,
                initialfile="output.html",
            )
        else:
            path = filedialog.askopenfilename(
                title="Select file",
                filetypes=self._filetypes,
            )
        if path:
            self.path_var.set(path)

    @property
    def value(self) -> str:
        return self.path_var.get()


class XSLTApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("XSLT-Transformer")
        self.geometry("700x560")
        self.minsize(600, 500)
        self.configure(fg_color="#161928")
        self._build_ui()

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color="#0f1120", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="✦  XSLT-Transformer",
            font=ctk.CTkFont("Segoe UI", 20, "bold"),
            text_color=ACCENT,
        ).pack(pady=(14, 2))

        ctk.CTkLabel(
            header,
            text="XML + XSL → HTML",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color=TEXT_DIM,
        ).pack()

        # ── Body ──────────────────────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=28, pady=20)

        # XML input
        self.row_xml = FileRow(
            body,
            icon="📄",
            label="XML File  (input)",
            filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")],
        )
        self.row_xml.pack(fill="x", pady=(0, 12))

        # XSL stylesheet
        self.row_xsl = FileRow(
            body,
            icon="🎨",
            label="XSL Stylesheet  (XSL / XSLT)",
            filetypes=[("XSL Files", "*.xsl *.xslt"), ("All Files", "*.*")],
        )
        self.row_xsl.pack(fill="x", pady=(0, 12))

        # Output file
        self.row_out = FileRow(
            body,
            icon="💾",
            label="Output File  (result)",
            filetypes=[("HTML", "*.html"), ("XML", "*.xml"), ("All Files", "*.*")],
            save=True,
        )
        default_out = os.path.join(os.path.expanduser("~"), "output.html")
        self.row_out.path_var.set(default_out)
        self.row_out.pack(fill="x", pady=(0, 20))

        # Transform button
        self.btn = ctk.CTkButton(
            body,
            text="⚡   Transform",
            font=ctk.CTkFont("Segoe UI", 15, "bold"),
            height=50,
            corner_radius=12,
            fg_color=ACCENT,
            hover_color=ACCENT_HOV,
            text_color="white",
            command=self._start_transform,
        )
        self.btn.pack(fill="x")

        # ── Footer: status bar + progress ─────────────────────────────
        footer = ctk.CTkFrame(self, fg_color="#0f1120", corner_radius=0, height=52)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        self.status_lbl = ctk.CTkLabel(
            footer,
            text="Select your files and click Transform.",
            font=ctk.CTkFont("Segoe UI", 12),
            text_color=TEXT_DIM,
            anchor="w",
        )
        self.status_lbl.place(x=20, rely=0.3, anchor="w")

        self.progress = ctk.CTkProgressBar(
            footer,
            height=5,
            corner_radius=0,
            fg_color="#1e2130",
            progress_color=ACCENT,
            mode="indeterminate",
        )
        self.progress.place(x=0, rely=1.0, anchor="sw", relwidth=1.0)
        self.progress.set(0)

    # ── Transformation ─────────────────────────────────────────────────────
    def _start_transform(self):
        if not self.row_xml.value or not self.row_xsl.value:
            self._set_status("⚠  Please select an XML file and an XSL stylesheet before proceeding.", AMBER)
            return
        self.btn.configure(state="disabled", text="Processing…")
        self.progress.start()
        self._set_status("Applying XSLT transformation…", ACCENT)
        threading.Thread(target=self._run_transform, daemon=True).start()

    def _run_transform(self):
        try:
            xml_doc = ET.parse(self.row_xml.value)
            xsl_doc = ET.parse(self.row_xsl.value)
            result  = ET.XSLT(xsl_doc)(xml_doc)
            out = self.row_out.value or os.path.join(os.path.expanduser("~"), "output.html")
            with open(out, "wb") as f:
                f.write(ET.tostring(result, pretty_print=True, encoding="UTF-8"))
            self.after(0, self._on_success, out)
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _on_success(self, out_file):
        self.progress.stop()
        self.progress.set(1)
        self.btn.configure(state="normal", text="⚡   Transform")
        self._set_status(f"✅  Saved to: {out_file}", GREEN)
        messagebox.showinfo("Transformation complete",
                            f"File generated successfully:\n{out_file}")

    def _on_error(self, msg):
        self.progress.stop()
        self.progress.set(0)
        self.btn.configure(state="normal", text="⚡   Transform")
        self._set_status(f"❌  Error: {msg}", RED)
        messagebox.showerror("Transformation error", msg)

    def _set_status(self, text, color=None):
        self.status_lbl.configure(text=text, text_color=color or TEXT_DIM)


if __name__ == "__main__":
    app = XSLTApp()
    app.mainloop()