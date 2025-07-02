"""
Console application interface for Mod Translator.
This module provides a user-friendly form-based terminal interface.
"""

import os
import sys
from typing import Dict, Any
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.theme import Theme
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich import box
from pyfiglet import Figlet

from ..commands.translate import (
    Settings, 
    handle_translate_command,
    log_title, 
    log_subtitle, 
    log_message, 
    DISABLE_LOGS
)

# Setup console and theme
UI_THEME = Theme({
    "primary": "white",
    "secondary": "bright_black",
    "accent": "red",
    "warning": "bold red",
    "error": "bold red",
})

QUESTIONARY_STYLE = questionary.Style([
    ("qmark", "fg:#FF5555 bold"),
    ("question", "fg:#FFFFFF"),
    ("answer", "fg:#AAAAAA"),
    ("pointer", "fg:#666666 bold"),
    ("highlighted", "fg:#FF5555 bold"),
    ("selected", "fg:#AAAAAA"),
    ("separator", "fg:#AAAAAA"),
    ("instruction", "fg:#AAAAAA"),
    ("text", "fg:#AAAAAA"),
])

# Create a rich console for fancy output
console = Console(theme=UI_THEME)

def display_title() -> None:
    """Display the application title using figlet."""
    # Clear the console before showing the title
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Set the console window title
    if os.name == 'nt':
        os.system('title Minecraft Mod Translator')

    f = Figlet(font='chunky')
    title1 = f.renderText('Minecraft Mod')
    title2 = f.renderText('Translator')
    console.print(Align.center(Text(title1, style="bold red")))
    console.print(Align.center(Text(title2, style="bold red")))
    console.print(Align.center(Text("Translate your Minecraft mods from one language to another", style="italic")))
    console.print()

def get_user_input() -> Dict[str, Any]:
    """Collect user input through a form interface."""
    try:
        # Prepare common language options
        language_options = [
            {'name': 'Afrikaans (af_ZA)', 'value': 'af_ZA'},
            {'name': 'Albanian (sq_AL)', 'value': 'sq_AL'},
            {'name': 'Arabic (ar_SA)', 'value': 'ar_SA'},
            {'name': 'Armenian (hy_AM)', 'value': 'hy_AM'},
            {'name': 'Asturian (ast_ES)', 'value': 'ast_ES'},
            {'name': 'Azerbaijani (az_AZ)', 'value': 'az_AZ'},
            {'name': 'Basque (eu_ES)', 'value': 'eu_ES'},
            {'name': 'Belarusian (be_BY)', 'value': 'be_BY'},
            {'name': 'Bosnian (bs_BA)', 'value': 'bs_BA'},
            {'name': 'Bulgarian (bg_BG)', 'value': 'bg_BG'},
            {'name': 'Catalan (ca_ES)', 'value': 'ca_ES'},
            {'name': 'Chinese Simplified (zh_CN)', 'value': 'zh_CN'},
            {'name': 'Chinese Traditional (zh_TW)', 'value': 'zh_TW'},
            {'name': 'Cornish (kw_GB)', 'value': 'kw_GB'},
            {'name': 'Croatian (hr_HR)', 'value': 'hr_HR'},
            {'name': 'Czech (cs_CZ)', 'value': 'cs_CZ'},
            {'name': 'Danish (da_DK)', 'value': 'da_DK'},
            {'name': 'Dutch (nl_NL)', 'value': 'nl_NL'},
            {'name': 'English United States (en_US)', 'value': 'en_US'},
            {'name': 'English Australia (en_AU)', 'value': 'en_AU'},
            {'name': 'English Canada (en_CA)', 'value': 'en_CA'},
            {'name': 'English New Zealand (en_NZ)', 'value': 'en_NZ'},
            {'name': 'English United Kingdom (en_GB)', 'value': 'en_GB'},
            {'name': 'Esperanto (eo_UY)', 'value': 'eo_UY'},
            {'name': 'Estonian (et_EE)', 'value': 'et_EE'},
            {'name': 'Faroese (fo_FO)', 'value': 'fo_FO'},
            {'name': 'Filipino (fil_PH)', 'value': 'fil_PH'},
            {'name': 'Finnish (fi_FI)', 'value': 'fi_FI'},
            {'name': 'French France (fr_FR)', 'value': 'fr_FR'},
            {'name': 'French Canada (fr_CA)', 'value': 'fr_CA'},
            {'name': 'Frisian (fy_NL)', 'value': 'fy_NL'},
            {'name': 'Galician (gl_ES)', 'value': 'gl_ES'},
            {'name': 'Georgian (ka_GE)', 'value': 'ka_GE'},
            {'name': 'German (de_DE)', 'value': 'de_DE'},
            {'name': 'Greek (el_GR)', 'value': 'el_GR'},
            {'name': 'Hawaiian (haw)', 'value': 'haw'},
            {'name': 'Hebrew (he_IL)', 'value': 'he_IL'},
            {'name': 'Hindi (hi_IN)', 'value': 'hi_IN'},
            {'name': 'Hungarian (hu_HU)', 'value': 'hu_HU'},
            {'name': 'Icelandic (is_IS)', 'value': 'is_IS'},
            {'name': 'Indonesian (id_ID)', 'value': 'id_ID'},
            {'name': 'Irish (ga_IE)', 'value': 'ga_IE'},
            {'name': 'Italian (it_IT)', 'value': 'it_IT'},
            {'name': 'Japanese (ja_JP)', 'value': 'ja_JP'},
            {'name': 'Kabyle (kab_DZ)', 'value': 'kab_DZ'},
            {'name': 'Kannada (kn_IN)', 'value': 'kn_IN'},
            {'name': 'Korean (ko_KR)', 'value': 'ko_KR'},
            {'name': 'Kölsch/Ripuarian (ksh_DE)', 'value': 'ksh_DE'},
            {'name': 'Latin (la_VA)', 'value': 'la_VA'},
            {'name': 'Latvian (lv_LV)', 'value': 'lv_LV'},
            {'name': 'Limburgish (li_LI)', 'value': 'li_LI'},
            {'name': 'Lithuanian (lt_LT)', 'value': 'lt_LT'},
            {'name': 'Low German (nds_DE)', 'value': 'nds_DE'},
            {'name': 'Luxembourgish (lb_LU)', 'value': 'lb_LU'},
            {'name': 'Macedonian (mk_MK)', 'value': 'mk_MK'},
            {'name': 'Malay (ms_MY)', 'value': 'ms_MY'},
            {'name': 'Maltese (mt_MT)', 'value': 'mt_MT'},
            {'name': 'Manx (gv_IM)', 'value': 'gv_IM'},
            {'name': 'Māori (mi_NZ)', 'value': 'mi_NZ'},
            {'name': 'Mohawk (moh_US)', 'value': 'moh_US'},
            {'name': 'Mongolian (mn_MN)', 'value': 'mn_MN'},
            {'name': 'Northern Sami (sme)', 'value': 'sme'},
            {'name': 'Norwegian Bokmål (no_NO)', 'value': 'no_NO'},
            {'name': 'Norwegian Nynorsk (nn_NO)', 'value': 'nn_NO'},
            {'name': 'Nuu-chah-nulth (nuk)', 'value': 'nuk'},
            {'name': 'Occitan (oc_FR)', 'value': 'oc_FR'},
            {'name': 'Ojibwe (oj_CA)', 'value': 'oj_CA'},
            {'name': 'Persian (fa_IR)', 'value': 'fa_IR'},
            {'name': 'Polish (pl_PL)', 'value': 'pl_PL'},
            {'name': 'Portuguese Portugal (pt_PT)', 'value': 'pt_PT'},
            {'name': 'Portuguese Brazil (pt_BR)', 'value': 'pt_BR'},
            {'name': 'Romanian (ro_RO)', 'value': 'ro_RO'},
            {'name': 'Russian (ru_RU)', 'value': 'ru_RU'},
            {'name': 'Scottish Gaelic (gd_GB)', 'value': 'gd_GB'},
            {'name': 'Serbian (sr_SP)', 'value': 'sr_SP'},
            {'name': 'Slovak (sk_SK)', 'value': 'sk_SK'},
            {'name': 'Slovenian (sl_SI)', 'value': 'sl_SI'},
            {'name': 'Somali (so_SO)', 'value': 'so_SO'},
            {'name': 'Spanish Spain (es_ES)', 'value': 'es_ES'},
            {'name': 'Spanish Argentina (es_AR)', 'value': 'es_AR'},
            {'name': 'Spanish Chile (es_CL)', 'value': 'es_CL'},
            {'name': 'Spanish Mexico (es_MX)', 'value': 'es_MX'},
            {'name': 'Spanish Uruguay (es_UY)', 'value': 'es_UY'},
            {'name': 'Spanish Venezuela (es_VE)', 'value': 'es_VE'},
            {'name': 'Swedish (sv_SE)', 'value': 'sv_SE'},
            {'name': 'Thai (th_TH)', 'value': 'th_TH'},
            {'name': 'Turkish (tr_TR)', 'value': 'tr_TR'},
            {'name': 'Ukrainian (uk_UA)', 'value': 'uk_UA'},
            {'name': 'Vietnamese (vi_VN)', 'value': 'vi_VN'},
            {'name': 'Welsh (cy_GB)', 'value': 'cy_GB'}
        ]
        
        # Create a lookup dictionary for language names
        language_names = {option["value"]: option["name"] for option in language_options}
        
        # Get the mods path
        mods_path = questionary.text(
            "Path to mod or mods folder:",
            default=os.path.join(os.getcwd(), "mods"),
            style=QUESTIONARY_STYLE
        ).ask()
        
        if mods_path is None:  # This occurs when user presses Ctrl+C
            sys.exit(0)
            
        if not mods_path:
            console.print("[bold red]Path is required. Exiting.[/bold red]")
            sys.exit(1)
        
        # Make sure path exists
        if not os.path.exists(mods_path):
            console.print(f"[bold red]Path '{mods_path}' does not exist. Exiting.[/bold red]")
            sys.exit(1)
        
        # Normalize path
        mods_path = os.path.abspath(mods_path)
          # Get source language - using English (en_US) as default
        # Find the en_US option to use as default
        default_source = next((option for option in language_options if option["value"] == "en_US"), language_options[0])
        
        source_lang = questionary.select(
            "Source language:",
            choices=language_options,
            default=default_source,
            instruction="(Use ↑↓ and Enter, or type to search)",
            style=QUESTIONARY_STYLE,
            use_jk_keys=False,
            use_search_filter=True
        ).ask()
        
        if source_lang is None:  # This occurs when user presses Ctrl+C
            sys.exit(0)
        
        # Get target language - filter out the source language
        target_language_options = [option for option in language_options if option["value"] != source_lang]
        
        # Find the first available option as default
        default_target = target_language_options[0]
        
        target_lang = questionary.select(
            "Target language:",
            choices=target_language_options,
            default=default_target,
            instruction="(Use ↑↓ and Enter, or type to search)",
            style=QUESTIONARY_STYLE,
            use_jk_keys=False, 
            use_search_filter=True
        ).ask()
        
        if target_lang is None:  # This occurs when user presses Ctrl+C
            sys.exit(0)
        
        # Check if OpenAI is available for translation method selection
        openai_available = False
        openai_status_message = ""
        
        try:
            import openai
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
            
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai_available = True
                openai_status_message = "✅ Available (API key configured)"
            else:
                openai_status_message = "❌ API key not found (.env file or environment variable)"
        except ImportError:
            openai_status_message = "❌ Package not installed (pip install openai python-dotenv)"
        
        # Get translation method
        translation_choices = [
            {"name": f"🌐 Google Translate (Free) - Always available", "value": "google"},
        ]
        
        if openai_available:
            translation_choices.append(
                {"name": f"🤖 OpenAI Translation (Premium) - {openai_status_message}", "value": "openai"}
            )
        else:
            translation_choices.append(
                {"name": f"🤖 OpenAI Translation (Premium) - {openai_status_message}", "value": "openai_unavailable"}
            )
        
        translation_method = questionary.select(
            "Choose translation method:",
            choices=translation_choices,
            default=translation_choices[0],
            instruction="(Use ↑↓ and Enter)",
            style=QUESTIONARY_STYLE,
            use_jk_keys=False
        ).ask()
        
        if translation_method is None:  # This occurs when user presses Ctrl+C
            sys.exit(0)
        
        # Handle OpenAI unavailable selection
        if translation_method == "openai_unavailable":
            console.print("\n[bold yellow]OpenAI Translation Setup Required[/bold yellow]")
            console.print("To use OpenAI translation, you need to:")
            console.print("1. Install dependencies: [cyan]pip install openai python-dotenv[/cyan]")
            console.print("2. Get an API key from: [cyan]https://platform.openai.com/api-keys[/cyan]")
            console.print("3. Create a [cyan].env[/cyan] file with: [cyan]OPENAI_API_KEY=your_key_here[/cyan]")
            console.print("\nFalling back to Google Translate...\n")
            translation_method = "google"
        
        use_ai = translation_method == "openai"
        
        # Get output path
        output_choice = questionary.select(
            "Where to save translated mods?",
            choices=[
                {"name": "Replace original mods", "value": "replace"},
                {"name": "Save to a different folder", "value": "new_folder"}
            ],
            instruction="(Use ↑↓ and Enter, or type to search)",
            style=QUESTIONARY_STYLE,
            use_jk_keys=False,
            use_search_filter=True
        ).ask()
        
        if output_choice is None:  # This occurs when user presses Ctrl+C
            sys.exit(0)
        
        output_path = mods_path
        if output_choice == "new_folder":
            # Get the output path for translated mods
            default_output = os.path.join(os.path.dirname(mods_path), "translated_mods")
            output_path = questionary.text(
                "Output folder path:",
                default=default_output,
                style=QUESTIONARY_STYLE
            ).ask()
            
            if output_path is None:  # This occurs when user presses Ctrl+C
                sys.exit(0)
            
            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
        
        # Clear the console before showing confirmation
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Confirm user choices with rich formatting
        console.print("\n[bold]Please confirm your choices:[/bold]")
        
        confirmation_table = Table(show_header=False, box=box.SIMPLE)
        confirmation_table.add_column("Parameter", style="secondary")
        confirmation_table.add_column("Value", style="primary")
        
        confirmation_table.add_row("Mods path", mods_path)
        confirmation_table.add_row("Source language", language_names.get(source_lang, source_lang))
        confirmation_table.add_row("Target language", language_names.get(target_lang, target_lang))
        confirmation_table.add_row("Translation method", "🤖 OpenAI (Premium)" if use_ai else "🌐 Google Translate (Free)")
        confirmation_table.add_row("Output path", output_path)
        
        console.print(confirmation_table)
        console.print()
        
        confirmed = questionary.confirm(
            "Continue with these settings?", 
            default=True,
            style=QUESTIONARY_STYLE,
        ).ask()
        
        if confirmed is None or not confirmed:  # This occurs when user presses Ctrl+C or selects No
            sys.exit(0)
        
        # Clear the console after confirmation
        os.system('cls' if os.name == 'nt' else 'clear')
        
        return {
            "path": mods_path,
            "source": source_lang,
            "target": target_lang,
            "output": output_path,
            "ai": use_ai
        }
    except KeyboardInterrupt:
        # Silently exit on Ctrl+C without showing any error message
        sys.exit(0)

def run_translation(params: Dict[str, Any]) -> None:
    """Run the translation process with the given parameters."""
    try:
        # Override the default logging functions to use rich
        global DISABLE_LOGS
        DISABLE_LOGS = True  # Disable built-in logging
        
        class Args:
            """Simple class to mimic argparse.Namespace."""
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        args = Args(**params)
          # Create progress display
        with Progress(
            SpinnerColumn(style="red"),
            TextColumn("[bold red]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("[red]Unpacking mod files...", total=None)# Define custom logging functions to update progress
            def custom_log_title(message):
                progress.update(task, description=f"[bold red]{message}")
            
            def custom_log_subtitle(message):
                # Display subtitles in the console using simple print
                print(f"  ↳ {message}")
            
            def custom_log_message(message):
                # Display log messages using simple print
                print(f"    • {message}")
            
            # Monkey-patch the logging functions
            from ..commands import translate
            translate.log_title = custom_log_title
            translate.log_subtitle = custom_log_subtitle
            translate.log_message = custom_log_message
            
            try:
                # Run the translation process
                handle_translate_command(args)
            except KeyboardInterrupt:
                # Silently exit on Ctrl+C without showing any error message
                sys.exit(0)
                
          # Show completion message with panel
        success_message = "[bold]Translation completed successfully![/bold]\n"
        success_message += f"Translated mods can be found at: [white]{params['output']}[/white]"
        
        console.print(Panel(
            success_message,
            title="Success",
            border_style="red",
            title_align="center",
            box=box.DOUBLE
        ))
    except KeyboardInterrupt:
        # Silently exit on Ctrl+C without showing any error message
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"[bold]{str(e)}[/bold]",
            title="Error",
            border_style="red",
            title_align="center",
            box=box.DOUBLE
        ))
        console.print_exception()

def main() -> None:
    """Main entry point for the console app."""
    try:
        display_title()
        
        # Check if deep-translator is installed
        try:
            from deep_translator import GoogleTranslator
        except ImportError:
            console.print(Panel(
                "[bold]deep_translator package is required for translation.[/bold]\n"
                "Please install it with: [cyan]pip install deep_translator[/cyan]",
                title="Missing Dependency",
                border_style="red",
                title_align="center",
                box=box.DOUBLE
            ))
            return
        
        params = get_user_input()
        
        # Additional check for OpenAI if AI translation was selected
        if params.get("ai", False):
            try:
                import openai
                try:
                    from dotenv import load_dotenv
                    load_dotenv()
                except ImportError:
                    pass
                
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    console.print(Panel(
                        "[bold]OpenAI API key not found![/bold]\n"
                        "To use OpenAI translation:\n"
                        "1. Get an API key from: [cyan]https://platform.openai.com/api-keys[/cyan]\n"
                        "2. Create a [cyan].env[/cyan] file with: [cyan]OPENAI_API_KEY=your_key_here[/cyan]\n"
                        "3. Or set the environment variable: [cyan]OPENAI_API_KEY=your_key[/cyan]",
                        title="OpenAI Setup Required",
                        border_style="red",
                        title_align="center",
                        box=box.DOUBLE
                    ))
                    return
            except ImportError:
                console.print(Panel(
                    "[bold]OpenAI package not found![/bold]\n"
                    "Please install it with: [cyan]pip install openai python-dotenv[/cyan]",
                    title="Missing OpenAI Dependencies",
                    border_style="red",
                    title_align="center",
                    box=box.DOUBLE
                ))
                return
        
        run_translation(params)
    except KeyboardInterrupt:
        # Silently exit on Ctrl+C without showing any error message
        sys.exit(0)
    except Exception as e:
        console.print(Panel(
            f"[bold]{str(e)}[/bold]",
            title="Error",
            border_style="red",
            title_align="center",
            box=box.DOUBLE
        ))
        console.print_exception()

if __name__ == "__main__":
    main()
