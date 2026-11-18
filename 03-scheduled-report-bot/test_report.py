from unittest.mock import patch
import main

with patch("main.send_line_notify") as mock_send:
    main.run_report()
    print("send_line_notify called with:", mock_send.call_args)
