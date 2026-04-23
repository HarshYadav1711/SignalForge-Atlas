class ApifyAdapter:
    """
    Placeholder adapter for Apify integration.

    Exists to provide a clear integration boundary for scalable data ingestion.
    Currently unused to preserve free, dependency-free execution.
    """

    def fetch(self, *args, **kwargs):
        raise NotImplementedError("Apify integration not enabled in local mode")
