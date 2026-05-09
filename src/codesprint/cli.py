"""
Command-line interface for CodeSprint.

Provides the main entry point and argument parsing.
"""

import argparse
import sys
import os
from typing import Optional, List

from codesprint import __version__
from codesprint.runner import CodeRunner
from codesprint.detector import LanguageDetector
from codesprint.executor import Executor
from codesprint.history import HistoryManager
from codesprint.formatter import OutputFormatter


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="codesprint",
        description="🚀 CodeSprint - Lightweight Multi-Language Code Snippet Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codesprint script.py                  Run Python file
  codesprint -c "print('Hello!')"       Run inline code
  codesprint -l js -c "console.log(1)"  Run JavaScript
  codesprint -i                         Interactive mode
  codesprint -H                         Show history
  codesprint -L                         List runtimes

Supported Languages:
  Python, JavaScript, TypeScript, Go, Rust, Java, C, C++,
  Ruby, PHP, Bash, Perl, Lua, R, Kotlin, Swift, Scala
        """,
    )
    
    # Positional argument for file
    parser.add_argument(
        "file",
        nargs="?",
        help="Source file to execute",
    )
    
    # Code input
    parser.add_argument(
        "-c", "--code",
        type=str,
        help="Code to execute (inline)",
    )
    
    # Language specification
    parser.add_argument(
        "-l", "--lang",
        type=str,
        help="Specify programming language",
    )
    
    # Timeout
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=30.0,
        help="Execution timeout in seconds (default: 30)",
    )
    
    # History options
    parser.add_argument(
        "-H", "--history",
        action="store_true",
        help="Show execution history",
    )
    
    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        help="Show history statistics",
    )
    
    parser.add_argument(
        "--clear-history",
        action="store_true",
        help="Clear all history",
    )
    
    # Interactive mode
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive REPL mode",
    )
    
    # List runtimes
    parser.add_argument(
        "-L", "--list",
        action="store_true",
        help="List available runtimes",
    )
    
    # Version
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Show version",
    )
    
    # No color
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    
    # Output format
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    
    return parser


def run_interactive(runner: CodeRunner, formatter: OutputFormatter) -> None:
    """Run interactive REPL mode."""
    print(formatter.format_header("🚀 CodeSprint Interactive Mode"))
    print("Type code and press Enter to execute. Type 'exit' or 'quit' to exit.\n")
    
    detector = LanguageDetector()
    
    while True:
        try:
            # Get code input
            print(formatter._colorize(">>> ", formatter.formatter.color_map.get("keyword", "")))
            code = input().strip()
            
            if not code:
                continue
            
            if code.lower() in ("exit", "quit"):
                print(formatter._colorize("\n👋 Goodbye!", formatter.formatter.color_map.get("keyword", "")))
                break
            
            # Detect language and run
            language, _ = detector.detect(code)
            result = runner.run(code, language=language)
            
            # Display result
            print(formatter.format_result(
                output=result.output,
                error=result.error,
                success=result.success,
                execution_time=result.execution_time,
                language=result.language,
            ))
            print()
            
        except KeyboardInterrupt:
            print(formatter._colorize("\n\n👋 Goodbye!", formatter.formatter.color_map.get("keyword", "")))
            break
        except EOFError:
            break


def show_history(formatter: OutputFormatter, limit: int = 20) -> None:
    """Show execution history."""
    history = HistoryManager()
    entries = history.load_history()[:limit]
    
    print(formatter.format_header("📜 Execution History"))
    
    if not entries:
        print(formatter._colorize("  No history entries", formatter.formatter.color_map.get("comment", "")))
        return
    
    for entry in entries:
        preview = entry.code.split("\n")[0][:60]
        print(formatter.format_history_entry(
            entry_id=entry.id,
            language=entry.language,
            success=entry.success,
            timestamp=entry.timestamp,
            preview=preview,
        ))
        print()


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Determine color usage
    use_color = not args.no_color if hasattr(args, "no_color") else True
    
    formatter = OutputFormatter(use_color=use_color)
    
    # Show version
    if args.version:
        print(f"CodeSprint v{__version__}")
        return 0
    
    # List runtimes
    if args.list:
        executor = Executor()
        runtimes = executor.list_available()
        print(formatter.format_available_runtimes(runtimes))
        return 0
    
    # Show history
    if args.history:
        show_history(formatter)
        return 0
    
    # Show stats
    if args.stats:
        history = HistoryManager()
        stats = history.get_stats()
        print(formatter.format_stats(stats))
        return 0
    
    # Clear history
    if args.clear_history:
        history = HistoryManager()
        history.clear_history()
        print(formatter._colorize("✓ History cleared", formatter.formatter.color_map.get("keyword", "")))
        return 0
    
    # Interactive mode
    if args.interactive:
        runner = CodeRunner(timeout=args.timeout, use_color=use_color)
        run_interactive(runner, formatter)
        return 0
    
    # Run code from file
    if args.file:
        runner = CodeRunner(timeout=args.timeout, use_color=use_color)
        result = runner.run_file(args.file, language=args.lang)
        
        if args.json:
            import json
            output = {
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "exit_code": result.exit_code,
                "execution_time": result.execution_time,
                "language": result.language,
            }
            print(json.dumps(output, indent=2))
        else:
            print(formatter.format_result(
                output=result.output,
                error=result.error,
                success=result.success,
                execution_time=result.execution_time,
                language=result.language,
            ))
        
        return result.exit_code
    
    # Run inline code
    if args.code:
        runner = CodeRunner(timeout=args.timeout, use_color=use_color)
        result = runner.run(args.code, language=args.lang)
        
        if args.json:
            import json
            output = {
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "exit_code": result.exit_code,
                "execution_time": result.execution_time,
                "language": result.language,
            }
            print(json.dumps(output, indent=2))
        else:
            print(formatter.format_result(
                output=result.output,
                error=result.error,
                success=result.success,
                execution_time=result.execution_time,
                language=result.language,
            ))
        
        return result.exit_code
    
    # No arguments - show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
