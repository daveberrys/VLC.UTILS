from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, ProgressBar, Static


class VlcTui(App):
    CSS = """
    Screen {
        align: center middle;
        background: #121212;
    }
    #mainContainer {
        width: 37;
        height: auto;
        border: thick $primary;
        padding: 1 2;
        background: #1e1e1e;
    }
    .label {
        width: 100%;
        content-align: center middle;
        margin-bottom: 0;
    }
    #trackProgress {
        width: 1fr;
        margin: 1 0;
    }
    """
    BINDINGS = [("q", "quit", "Quit VLC Utils")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="mainContainer"):
            yield Static("VLC.UTILS", id="title", classes="label")
            yield Static("Awaiting VLC connection...", id="songInfo", classes="label")
            yield Static("-", id="albumInfo", classes="label")
            yield Static("-", id="artistInfo", classes="label")
            yield ProgressBar(id="trackProgress", show_percentage=False, show_eta=False)
            yield Static("00:00 / 00:00", id="timeInfo", classes="label")
            yield Static("State: stopped", id="statusInfo", classes="label")
        yield Footer()

    def formatTime(self, seconds):
        mins, secs = divmod(int(seconds), 60)
        return f"{mins:02}:{secs:02}"

    def updateInfo(self, stats, artUrl):
        self.query_one("#songInfo").update(f"{stats['title']}")
        self.query_one("#albumInfo").update(f"{stats['album']}")
        self.query_one("#artistInfo").update(f"{stats['artist']}")
        self.query_one("#statusInfo").update(f"State: {stats['state']}")

        currentTime = self.formatTime(stats["position"])
        totalTime = self.formatTime(stats["length"])
        self.query_one("#timeInfo").update(f"{currentTime} / {totalTime}")

        bar = self.query_one("#trackProgress")
        bar.total = stats["length"]
        bar.progress = stats["position"]


if __name__ == "__main__":
    app = VlcTui()
    app.run()
