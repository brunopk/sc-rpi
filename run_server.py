#!/usr/bin/env python
import sys

if __name__ == '__main__':
    sys.path.append('./src')
    
    import logging

    from main import build_websocket_handler
    from helpers import configure_logging, configure_status_led, configure_zeroconf, load_config, turn_led_indicator_on, turn_led_indicator_off, cleanup_gpio
    from scapy.all import IP, ICMP, sr1
    from aiohttp import web
    from hardware_controller import HardwareController
    
    config = load_config()
    host = config['DEFAULT'].get('host', '0.0.0.0')
    port = int(config['DEFAULT'].get('port', str(8080)))
    default_gateway = config['CONNECTION_CHECK'].get('default_gateway')
    iface = config['CONNECTION_CHECK'].get('iface')
    timeout = float(config['CONNECTION_CHECK'].get('timeout'))
    status_led = int(config['CONNECTION_CHECK'].get('status_led'))

    configure_logging(config)
    configure_status_led(config)
    configure_zeroconf()

    # Using the controller to handle the strip is thread-safe under the assumption that there's only one thread managing the event loop.
    hw_controller = HardwareController(config)

    exit_code = 0
    logger = logging.getLogger("main")

    try:
        turn_led_indicator_off(status_led)
        reply = sr1(IP(dst=default_gateway)/ICMP(), iface=iface, timeout=timeout, verbose=False)
        if reply is None: 
            raise Exception(f"No answer from {default_gateway}")
        turn_led_indicator_on(status_led)

        
        app = web.Application()
        app.add_routes([web.get('/', build_websocket_handler(hw_controller))])
        web.run_app(app, print=logger.info, port=port, host=host)

    except KeyboardInterrupt as e:
        logger.info('Finalizing server')
        exit_code = 0
    except Exception as e:
        logger.exception(e)
        exit_code = 1
    finally:
        cleanup_gpio()
        exit(exit_code)
