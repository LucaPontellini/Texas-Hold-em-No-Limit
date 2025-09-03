import sys
import time
import logging
import config

logger = logging.getLogger(__name__)

def timed_input(prompt: str, timeout: int) -> str:
    """
    Mostra `prompt` e attende al massimo `timeout` secondi.
    Restituisce la stringa letta (senza newline), altrimenti solleva TimeoutError.
    Supporta sia Unix (select) che Windows (msvcrt).
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()

    end_time = time.time() + timeout

    if sys.platform.startswith('win'):
        # Windows: usa msvcrt per leggere carattere per carattere
        import msvcrt
        buffer = ''
        while time.time() < end_time:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                # termina su Enter
                if ch in ('\r', '\n'):
                    sys.stdout.write('\n')
                    return buffer
                # backspace
                if ch == '\b':
                    buffer = buffer[:-1]
                    sys.stdout.write('\b \b')
                else:
                    buffer += ch
                    sys.stdout.write(ch)
                sys.stdout.flush()
            time.sleep(0.05)
        sys.stdout.write('\n')
        logger.info("timed_input: timeout expired after %ds", timeout)
        raise TimeoutError(f"Timed out after {timeout} seconds")

    else:
        # Unix: usa select su stdin
        import select
        reads, _, _ = select.select([sys.stdin], [], [], timeout)
        if reads:
            line = sys.stdin.readline()
            return line.rstrip('\n')
        else:
            logger.info("timed_input: timeout expired after %ds", timeout)
            sys.stdout.write('\n')
            raise TimeoutError(f"Timed out after {timeout} seconds")