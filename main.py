from sites import qmail, school, wife, bank

SITES = {
    (qmail, 6680),
    (school, 6673),
    (wife, 6691),
    (bank, 6603)
}

def main(debug=False):
    for package, port in SITES:
        app = getattr(getattr(package, "app"), "app")
        app.run(host="0.0.0.0", port=port, debug=debug)

if __name__ == "__main__":
    main(debug=True)
