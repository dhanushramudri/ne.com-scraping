import time
import threading
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.align import Align
from collections import defaultdict

console = Console()

BANNER = """
██╗  ██╗███████╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
╚██╗██╔╝██╔════╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
 ╚███╔╝ █████╗      ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
 ██╔██╗ ██╔══╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
██╔╝ ██╗███████╗    ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
"""

class XeTerminalUI:
    def __init__(self):
        self.stats = {
            "total_requests": 0,
            "completed_requests": 0,
            "total_rows": 0,
            "errors": 0,
            "current_source": "",
            "current_date": "",
            "start_time": time.time(),
        }
        self.source_progress = defaultdict(lambda: {"done": 0, "rows": 0})
        self.recent_logs = []
        self.live = None
        self._lock = threading.Lock()

    def _make_layout(self):
        # Stats table
        stats_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
        stats_table.add_column("Key", style="bold cyan", width=22)
        stats_table.add_column("Value", style="bold white")

        elapsed = int(time.time() - self.stats["start_time"])
        hours, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        elapsed_str = f"{hours:02d}:{mins:02d}:{secs:02d}"

        rate = self.stats["total_rows"] / max(elapsed, 1)

        stats_table.add_row("⏱  Elapsed", elapsed_str)
        stats_table.add_row("🌐  Requests Done", str(self.stats["completed_requests"]))
        stats_table.add_row("📦  Total Rows", f"[green]{self.stats['total_rows']:,}[/green]")
        stats_table.add_row("⚡  Rows/sec", f"{rate:.1f}")
        stats_table.add_row("❌  Errors", f"[red]{self.stats['errors']}[/red]")
        stats_table.add_row("📅  Current Date", self.stats["current_date"] or "-")
        stats_table.add_row("🔄  Current Source", self.stats["current_source"] or "-")

        # Source breakdown table
        source_table = Table(
            title="Source Currency Progress",
            box=box.ROUNDED,
            style="cyan",
            title_style="bold cyan",
            padding=(0, 1)
        )
        source_table.add_column("Currency", style="bold yellow", width=10)
        source_table.add_column("Requests", justify="right", width=10)
        source_table.add_column("Rows", justify="right", style="green", width=10)

        for src, data in sorted(self.source_progress.items()):
            source_table.add_row(src, str(data["done"]), f"{data['rows']:,}")

        # Recent activity log
        log_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
        log_table.add_column("Log", style="dim white")
        for entry in self.recent_logs[-8:]:
            log_table.add_row(entry)

        layout = Table.grid(padding=1)
        layout.add_column(ratio=1)
        layout.add_column(ratio=1)

        layout.add_row(
            Panel(stats_table, title="[bold green]Live Stats[/bold green]", border_style="green"),
            Panel(source_table, title="[bold yellow]Sources[/bold yellow]", border_style="yellow"),
        )
        layout.add_row(
            Panel(log_table, title="[bold blue]Recent Activity[/bold blue]", border_style="blue"),
            Panel(
                Align.center(
                    Text(f"{self.stats['total_rows']:,}\nrows collected", justify="center", style="bold green"),
                    vertical="middle"
                ),
                title="[bold green]Total Output[/bold green]",
                border_style="green",
                height=10
            )
        )
        return layout

    def log(self, msg: str):
        with self._lock:
            timestamp = time.strftime("%H:%M:%S")
            self.recent_logs.append(f"[dim]{timestamp}[/dim] {msg}")
            if len(self.recent_logs) > 50:
                self.recent_logs.pop(0)

    def start(self):
        # Print banner first
        console.print(f"[bold cyan]{BANNER}[/bold cyan]")
        console.print(
            Panel.fit(
                "[bold green]🚀 Scraping started![/bold green]  "
                "[dim]XE.com Exchange Rate Scraper[/dim]",
                border_style="green"
            )
        )
        console.print()

        self.live = Live(
            self._make_layout(),
            console=console,
            refresh_per_second=2,
            screen=False
        )
        self.live.start()

    def update(self):
        if self.live:
            with self._lock:
                self.live.update(self._make_layout())

    def stop(self):
        if self.live:
            self.live.stop()
        elapsed = int(time.time() - self.stats["start_time"])
        hours, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        console.print()
        console.print(
            Panel(
                f"[bold green]✅ Scraping complete![/bold green]\n\n"
                f"  [cyan]Total rows:[/cyan]     [bold white]{self.stats['total_rows']:,}[/bold white]\n"
                f"  [cyan]Requests done:[/cyan]  [bold white]{self.stats['completed_requests']:,}[/bold white]\n"
                f"  [cyan]Errors:[/cyan]         [bold red]{self.stats['errors']}[/bold red]\n"
                f"  [cyan]Time elapsed:[/cyan]   [bold white]{hours:02d}:{mins:02d}:{secs:02d}[/bold white]\n"
                f"  [cyan]Output file:[/cyan]    [bold yellow]xe_rates_output.csv[/bold yellow]",
                title="[bold green]Summary[/bold green]",
                border_style="green"
            )
        )

# Global singleton
ui = XeTerminalUI()