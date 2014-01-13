from sites import qmail, school

SITES = {
    (qmail, 6401),
    (school, 6402)
}

def main(debug=False):
    for package, port in SITES:
        app = getattr(getattr(package, "app"), "app")
        app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    main(debug=True)
