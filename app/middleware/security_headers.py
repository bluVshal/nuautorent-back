"""Response security headers.

Applied to every response via an after_request hook. These are the headers a
pen test / scanner (e.g. OWASP ZAP) checks for. HSTS is only sent when the
request arrives over HTTPS so it never breaks plain-HTTP local development.
"""


def register_security_headers(app):
    @app.after_request
    def _set_security_headers(response):
        # Stop MIME sniffing.
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Disallow framing (clickjacking protection). This is a JSON API.
        response.headers["X-Frame-Options"] = "DENY"
        # Minimal referrer leakage.
        response.headers["Referrer-Policy"] = "no-referrer"
        # Lock down what this API is allowed to do in a browser context.
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        # This is an API, not a website; disable powerful browser features.
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        # Advertise HTTPS-only to browsers, but only once we're actually on HTTPS.
        if request_is_secure():
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # Don't advertise the server software.
        response.headers["Server"] = "nuautorent"
        return response


def request_is_secure():
    from flask import request

    # Honour X-Forwarded-Proto when behind a reverse proxy/load balancer.
    forwarded_proto = request.headers.get("X-Forwarded-Proto", "")
    return request.is_secure or forwarded_proto.lower() == "https"
