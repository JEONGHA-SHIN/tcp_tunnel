import argparse
from . import create_exposed_app
from . import create_local_app

def main():
    parser = argparse.ArgumentParser(description='TCP Tunnel Server')
    parser.add_argument('--exposed', action='store_true', help='Run the exposed server')
    parser.add_argument('--local', action='store_true', help='Run the local server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')

    args = parser.parse_args()

    if args.exposed:
        app = create_exposed_app()
        app.run(port=args.port)
        
    elif args.local:
        app = create_local_app()
        app.run(port=args.port)

if __name__ == '__main__':
    main()


