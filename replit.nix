{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.setuptools
    pkgs.python310Packages.wheel

    # Core scientific stack
    pkgs.python310Packages.numpy
    pkgs.python310Packages.pandas

    # Dashboard and visualization
    pkgs.python310Packages.plotly
    pkgs.python310Packages.dash

    # API and alerts
    pkgs.python310Packages.requests
    pkgs.python310Packages.pyotp
    pkgs.python310Packages.websocket_client

    # Forecasting (optional)
    pkgs.python310Packages.prophet
  ];
}
