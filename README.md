# AdHunt

Web advertisement gathering and notification system.

---

Current institutes included in the collection service:
- Institute of Geophysics, ETH Zurich

Institutes planned to be included soon:
- [ ] Earth-Jobs website
- [ ] GeoForschungsZentrum (GFZ) Potsdam
- [ ] Institut de Physique du Globe de Paris (IPGP)

If you want to add a new institute to the service, choose 
one of the three options:
1. Open an issue on Github.
2. Communicate directly to me.
3. Contributing a snippet of code.
The interface has been so designed that the procedure should be simple.
You'll need:
    - If the institute you're interested in 
    has an html page / json response for the positions,
    directly write a function of how the information
    can be extracted. A model can be seen in `collect.collector.ethz_ifg_parser`
    - Add to `COLLECTOR_LIST` in `main.py`.
    - If the information is not in html/json format,
    you need to write a new class, as `collect.collector.HTMLCollector`.
    It should be a child of `collect.collector.Collector` class, and you
    only need to override its `get_positions` method.
