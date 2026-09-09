import vlc
import sys
import os
import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import box

console = Console()

# iptv-org API Endpoints
CHANNELS_URL = "https://iptv-org.github.io/api/channels.json"
STREAMS_URL = "https://iptv-org.github.io/api/streams.json"

current_results = {}
current_station_name = "None"
db_cache = []

def print_banner():
    banner_text = """
    ████████╗██╗   ██╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
    ╚══██╔══╝██║   ██║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
       ██║   ██║   ██║    ███████║███████║██║     █████╔╝ 
       ██║   ╚██╗ ██╔╝    ██╔══██║██╔══██║██║     ██╔═██╗ 
       ██║    ╚████╔╝     ██║  ██║██║  ██║╚██████╗██║  ██╗
       ╚═╝     ╚═══╝      ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
             G L O B A L   O P E N   T V
             BY WAQAR HASSAN
    """
    banner = Text(banner_text, style="bold cyan")
    console.print(Align.center(banner))

def display_status():
    status_text = Text()
    status_text.append(f"📺 Now Broadcasting: ", style="bold magenta")
    status_text.append(f"{current_station_name}\n", style="bold white")
    status_text.append(f"🖥️  Operator: ", style="bold magenta")
    status_text.append(f"Waqar Hassan | ONLINE", style="bold cyan")
    
    panel = Panel(status_text, title="[bold yellow]BROADCAST STATUS[/bold yellow]", border_style="cyan", box=box.ROUNDED)
    console.print(panel)

def load_databases():
    """Fetches and maps the channel names, filtering out dead links."""
    with console.status("[bold cyan]Initializing global databases from iptv-org...[/bold cyan]", spinner="dots"):
        try:
            channels_req = requests.get(CHANNELS_URL, timeout=10)
            streams_req = requests.get(STREAMS_URL, timeout=10)
            
            channels_data = channels_req.json()
            streams_data = streams_req.json()

            # Map streams, strictly ignoring known dead links
            stream_map = {}
            for stream in streams_data:
                ch_id = stream.get("channel")
                url = stream.get("url")
                status = stream.get("status")
                
                # Only save the stream if it is NOT marked as an error
                if ch_id and url and status not in ["error", "timeout"]:
                    stream_map[ch_id] = url
            
            global db_cache
            db_cache = [] # Reset cache
            for channel in channels_data:
                ch_id = channel.get("id")
                if ch_id in stream_map:
                    db_cache.append({
                        "id": ch_id,
                        "name": channel.get("name", "Unknown"),
                        "country": channel.get("country", "Unknown"),
                        "url": stream_map[ch_id]
                    })
                    
            console.print(f"[green]Database loaded! Found {len(db_cache)} verified active streams.[/green]")
        except Exception as e:
            console.print(f"[bold red]Uplink failed during database init: {e}[/bold red]")
            sys.exit(1)

def search_tv(query):
    """Searches the local cache for matching TV networks."""
    global current_results
    query = query.lower()
    
    table = Table(box=box.MINIMAL_DOUBLE_HEAD, style="magenta")
    table.add_column("ID", justify="center", style="bold cyan")
    table.add_column("Network Name", style="bold white")
    table.add_column("Region", style="yellow")
    
    results_dict = {}
    match_count = 0
    
    for channel in db_cache:
        if query in channel["name"].lower() or query in channel["country"].lower():
            match_count += 1
            str_id = str(match_count)
            results_dict[str_id] = channel
            table.add_row(str_id, channel["name"], channel["country"])
            if match_count >= 10000: # Limit output to keep terminal clean
                break
                
    if not results_dict:
        console.print(Panel("[bold red]ERROR: No networks found. Try a new keyword.[/bold red]", border_style="red"))
        return {}
        
    console.print(Panel(table, title=f"[bold yellow]SCAN RESULTS: {query.upper()}[/bold yellow]", border_style="magenta"))
    return results_dict

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    global current_results, current_station_name
    
    clear_screen()
    print_banner()
    load_databases()
    display_status()
    
    # Initialize VLC to open a visible window (not headless)
    # Forces massive cache and permits frame dropping to save CPU load
    instance = vlc.Instance("--network-caching=20000 --drop-late-frames --skip-frames --avcodec-hw=none --quiet")
    player = instance.media_player_new()
    
    while True:
        console.print("\n[bold yellow]COMMANDS:[/bold yellow] [cyan]search <term>[/cyan] | [cyan]play <id>[/cyan] | [cyan]stop[/cyan] | [cyan]exit[/cyan]")
        user_input = Prompt.ask("[bold magenta]waqar@tv:~#[/bold magenta]").strip().lower().split(maxsplit=1)
        
        if not user_input:
            continue
            
        command = user_input[0]
        
        if command == "search":
            if len(user_input) < 2:
                console.print("[red]Syntax Error: Provide a search term (e.g., search news, search uk).[/red]")
                continue
            current_results = search_tv(user_input[1])
            
        elif command == "play":
            if len(user_input) < 2:
                console.print("[red]Syntax Error: Provide a Target ID.[/red]")
                continue
                
            station_id = user_input[1]
            station_data = current_results.get(station_id)
            
            if not station_data:
                console.print(f"[red]Error: ID '{station_id}' invalid. Execute search first.[/red]")
                continue
                
            current_station_name = station_data['name']
            clear_screen()
            print_banner()
            display_status()
            
            media = instance.media_new(station_data['url'])
            player.set_media(media)
            player.play()
            
        elif command == "stop":
            current_station_name = "None"
            player.stop()
            clear_screen()
            print_banner()
            display_status()
            
        elif command == "exit":
            console.print("[bold red]Terminating broadcast session. Goodbye.[/bold red]")
            player.stop()
            sys.exit(0)
            
        else:
            console.print("[red]Command not recognized.[/red]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Session aborted.[/bold red]")
        sys.exit(0)
