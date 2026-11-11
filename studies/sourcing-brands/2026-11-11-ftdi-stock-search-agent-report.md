Status: COMPLETE (2026-11-11 06:55 UTC)

# FTDI FT231X stock search, 2026-11-11

Agent report for Northern Widget (Margay, Okapi). Read-only web research. Need: 100-300 FT231XQ-R (QFN-20 4x4); also FT231XS-R (SSOP-20), FT231XQ-T (tray), and any other FT231X ordering code.

Baseline from the caller (not re-fetched unless noted): Digi-Key 0 in stock 2026-11-11, FT231XQ-R 5,000 expected 18 Jan 2027, 50-week lead time; FT231XS-R 0, 2,000 expected 16 Mar 2027.

All times UTC. Numbers are quoted from the page as returned by the fetch tool; anything not confirmed is marked UNVERIFIED.

## Source log (every source checked, dead ends included)

| # | Source | URL | Fetched (UTC) | Result |
|---|--------|-----|---------------|--------|
| 1 | FTDI where-to-buy | https://ftdichip.com/where-to-buy/ | 06:27 | DEAD END: HTTP 403 |
| 2 | FTDI distributors | https://ftdichip.com/distributors/ | 06:28 | DEAD END: HTTP 403 |
| 3 | Mouser FT231XQ-R | https://www.mouser.com/ProductDetail/FTDI/FT231XQ-R | 06:27 | DEAD END: fetch timeout (60 s) |
| 4 | Octopart search | https://octopart.com/search?q=FT231XQ-R | 06:28 | DEAD END: HTTP 403 |
| 5 | FindChips FT231XQ-R | https://www.findchips.com/search/FT231XQ-R | 06:29 | OK: 8 rows, no authorized flags or timestamps in fetched text (rows below) |
| 6 | LCSC C132159 | https://www.lcsc.com/product-detail/C132159.html | 06:29 | PARTIAL: JS page; stock and price not in fetched text |
| 7 | TME FT231XQ-R | https://www.tme.eu/en/details/ft231xq-r/usb-interfaces-integrated-circuits/ftdi/ | 06:29 | OK: 0 in stock (row below) |
| 8 | Newark 83T7088 | https://www.newark.com/ftdi/ft231xq/usb-interface-transceiver-usb/dp/83T7088 | 06:29 | DEAD END: fetch timeout (60 s) |
| 9 | LCSC API / FTDI / Mouser / Newark via curl | (several) | 06:31 | DEAD END: shell fetch refused by this session's permission classifier; WebFetch only from here on |
| 10 | OEMsTrade FT231XQ-R | https://www.oemstrade.com/search/ft231xq-r | 06:31 | OK: authorized badges shown per row (rows below); page tail had one unlabeled 24,070-unit row |
| 11 | Oemsecrets compare | https://www.oemsecrets.com/compare/FT231XQ-R | 06:31 | DEAD END: HTTP 403 |
| 12 | Digi-Key keyword search | https://www.digikey.com/en/products/result?keywords=FT231X | 06:31 | DEAD END: fetched text held only navigation, no parts |
| 13 | Newark (alternate URL) | https://www.newark.com/ftdi/ft231xq-r/usb-interface-transceiver-usb/dp/83T7088 | 06:32 | DEAD END: fetch timeout (60 s) |
| 14 | OEMsTrade FT231XS-R | https://www.oemstrade.com/search/ft231xs-r | 06:33 | OK: authorized rows all 0 (rows below); page truncated at ~100k chars |
| 15 | OEMsTrade FT231XQ-T | https://www.oemstrade.com/search/ft231xq-t | 06:33 | OK: authorized rows all 0 (rows below) |
| 16 | Farnell UK 2081325 | https://uk.farnell.com/ftdi/ft231xq-r/usb-interface-transceiver-usb/dp/2081325 | 06:33 | DEAD END: fetch timeout (60 s) |
| 17 | Arrow FT231XQ-R | https://www.arrow.com/en/products/ft231xq-r/ftdi-chip | 06:34 | DEAD END: fetch timeout (60 s) |
| 18 | Future Electronics FT231XQ-R | https://www.futureelectronics.com/p/semiconductors--analog--interface--usb/ft231xq-r-ftdi-chip-4071060 | 06:34 | DEAD END: fetch timeout (60 s); URL was a guess, may not exist |
| 19 | FTDI regional sales pages (current and old2020) | https://ftdichip.com/?p=3256 ; https://www.ftdichip.com/old2020/SalesNetwork/NorthAmerica.htm | 06:35 | DEAD END: HTTP 403 |
| 20 | Wayback Machine copy of FTDI sales page | web.archive.org | 06:35 | DEAD END: fetch tool cannot reach web.archive.org |
| 21 | Web search snippets on FTDI sales network | (search) | 06:35 | Search summary only, NOT a fetched page: names Digi-Key, Arrow, Mouser, Farnell element14, GLYN, Macnica Galaxy across regional pages. UNVERIFIED |
| 22 | Andy's Chrome: ftdichip.com/where-to-buy | https://ftdichip.com/where-to-buy/ | 06:36 | DEAD END: Cloudflare "Performing security verification" page; not attempted further (no bot-check bypass) |
| 23 | Andy's Chrome: Mouser FT231XQ-R | https://www.mouser.com/ProductDetail/FTDI/FT231XQ-R | 06:37 | DEAD END: bot-protection interstitial ("Powered and protected by") |
| 24 | Andy's Chrome: Newark 83T7088 | https://www.newark.com/ftdi/ft231xq-r/usb-interface-transceiver-usb/dp/83T7088 | 06:37 | DEAD END: extension has no site permission for newark.com; Andy can allow it, Chrome use stopped here |
| 25 | Digi-Key product ID 3029155 | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XQ-R/3029155 | 06:38 | WRONG PART: page is FT230XS-R (768-1135), 0 in stock, "Estimated in-stock date unavailable". Discarded |
| 26 | FindChips FT231XS-R | https://www.findchips.com/search/FT231XS-R | 06:38 | OK (rows below) |
| 27 | FindChips FT231X (all codes) | https://www.findchips.com/search/FT231X | 06:38 | OK: 44 rows, 12 sellers, no authorized markers in fetched text (rows below) |
| 28 | Farnell export 2081325 | https://export.farnell.com/ftdi/ft231xq-r/usb-interface-transceiver-usb/dp/2081325 | 06:40 | DEAD END: fetch timeout (60 s) |
| 29 | Digi-Key FT231XQ-R 768-1128 (ID 3029154) | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XS-R/3029154 | 06:40 | OK: page is FT231XQ-R, 20-WFQFN (row below) |
| 30 | Digi-Key ID 4476318 | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XQ-T/4476318 | 06:40 | WRONG PART: HMC815LC5TR. Discarded |
| 31 | Digi-Key FT231XQ-T 768-1155-ND (ID 3749470) | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XQ-T/3749470 | 06:42 | OK (row below) |
| 32 | Digi-Key FT231XS-R 768-1129 (ID 3029139) | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XS-R/3029139 | 06:42 | OK (row below) |
| 33 | element14 Singapore 2081325 | https://sg.element14.com/ftdi/ft231xq-r/usb-interface-transceiver-usb/dp/2081325 | 06:43 | DEAD END: fetch timeout (60 s) |
| 34 | Avnet Americas (guessed URL) | https://www.avnet.com/americas/product/ftdi/ft231xq-r/evolve-58928373/ | 06:43 | DEAD END: HTTP 400 (URL guessed) |
| 35 | RS Ireland 757-0045 and 923-1613 | https://ie.rs-online.com/web/p/multiprotocol-transceivers/7570045 ; .../9231613 | 06:44 | DEAD END: HTTP 403. Search snippet only: 2-unit pack EUR 4.40 and 5,000-unit reel EUR 8,900, "in stock" per snippet. UNVERIFIED |
| 36 | CPC Farnell SC19129 | https://cpc.farnell.com/ftdi/ft231xq-r/i-f-usb2-0-fs-to-f-l-h-s-uart/dp/SC19129 | 06:44 | DEAD END: fetch timeout (60 s) |
| 37 | FindChips FT231XQ-T | https://www.findchips.com/search/FT231XQ-T | 06:44 | OK (rows below) |

| 38 | Newark short URL | https://www.newark.com/83T7088 | 06:47 | DEAD END: HTTP 403 |
| 39 | Web search on Newark 83T7088 | (search) | 06:47 | No Newark page in results. Snippet for RS Belgium/France 757-0045: "Temporairement en rupture de stock", 5,000 units expected to ship from 11 Nov 2026. UNVERIFIED (page 403 at 06:52) |
| 40 | RS UK 923-1613 | https://uk.rs-online.com/web/p/multiprotocol-transceivers/9231613 | 06:48 | DEAD END: HTTP 403 |
| 41 | Farnell Norway 2081330 | https://no.farnell.com/en-NO/ftdi/ft231xq-r/i-f-usb2-0-fs-to-f-l-h-s-uart/dp/2081330 | 06:48 | DEAD END: fetch timeout (60 s). Search snippet for CPC SC19129 says "No longer stocked" / "No Longer Manufactured": UNVERIFIED, and contradicts Digi-Key "Part Status: Active" |
| 42 | LCSC product-image page C132159 | https://www.lcsc.com/product-image/C132159.html | 06:48 | OK: "In-Stock: 20", 100+: $6.0052, Minimum 1 |
| 43 | PCX Co | https://pcxco.com/?p=600850 | 06:48 | DEAD END: HTTP 403 (snippet claims "IN STOCK - SHIPS IMMEDIATELY", $1.82; broker, UNVERIFIED) |
| 44 | SparkFun news 1629 | https://news.sparkfun.com/1629 | 06:50 | OK: counterfeit background (below) |
| 45 | FTDI counterfeit statement PDF | https://www.ftdichip.com/old2020/support/Documents/QualityDocuments/Counterfeit%20statement.pdf | 06:50 | DEAD END: HTTP 403 (search snippet: May 2014, advises buying from FTDI or an authorized distributor; UNVERIFIED) |
| 46 | Hackaday 2016-02-01 | https://hackaday.com/2016/02/01/ftdi-drivers-break-fake-chips-again/ | 06:51 | OK: counterfeit background (below) |
| 47 | Win Source product page | https://www.win-source.net/products/detail/ftdi/ft231xq-r.html | 06:51 | DEAD END: HTTP 403 (aggregator rows used instead) |
| 48 | FTDI Global Suppliers (old2020) | https://www.ftdichip.com/old2020/SalesNetwork/GlobalSuppliers.htm | 06:51 | DEAD END: HTTP 403. Search snippet says FTDI "can provide IC samples and evaluation kits to anywhere in the world"; 2020-era page, UNVERIFIED |
| 49 | SOS electronic FT231XQ-T | https://www.soselectronic.com/en-us/products/ftdi/ft231xq-t-131282 | 06:51 | DEAD END: HTTP 403 |
| 50 | Utmel | https://www.utmel.com/productdetail/ftdi-ft231xq-r | 06:51 | DEAD END: "Verifying you are human" page; not pursued |
| 51 | Rutronik24 (guessed URL) | https://www.rutronik24.com/product/ftdi/ft231xq-r/6418617.html | 06:52 | DEAD END: HTTP 410 (URL guessed); no Rutronik FT231X row found on any aggregator |
| 52 | AliExpress search | https://www.aliexpress.us/w/wholesale-FT231XQ.html | 06:52 | DEAD END: redirect to login page; not followed |
| 53 | Arrow es-mx FT231XQ-R; Arrow FT231XQ-T | https://www.arrow.com/es-mx/products/ft231xq-r/ftdi-chip ; https://www.arrow.com/en/products/ft231xq-t/ftdi-chip.html | 06:52 | DEAD END: fetch timeout (60 s). Search snippet (undated, likely stale): "No Stock Available", lead time 20 weeks, $2.15 at 5,000. UNVERIFIED |
| 54 | Avnet, Future Electronics | (search) | 06:52 | No FT231XQ-R stock row found on any page read; FindChips snippets mention Avnet and Arrow among authorized sellers. UNVERIFIED |

## Authorized distributors: confirmed rows

Authorized status here comes from the "ECIA (NEDA) Member / Authorized Distributor" badge OEMsTrade prints on the row, or from the distributor being a franchised FTDI catalog house (Digi-Key). FTDI's own distributor page could not be read (403 and Cloudflare check), so FTDI's list itself is UNVERIFIED.

| Part | Seller | SKU | Stock | Price at 100 | MOQ | Lead time / restock | Ships from / to US | Source, fetched (UTC, 2026-11-11) |
|------|--------|-----|-------|--------------|-----|---------------------|-------------------|----------------------------------|
| FT231XQ-R | Digi-Key | 768-1128-1-ND (CT) | "In-Stock: 0" | $2.20000 | 1 (CT); TR 5,000 at $1.76250 | "5,000 expected in stock on 18-Jan-2027"; "Manufacturer Standard Lead Time" 50 Weeks | US (Thief River Falls, MN) | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XS-R/3029154, 06:40 |
| FT231XQ-R | Newark | 83T7088 (CT), 83T7088RL (reel) | 4533 per OEMsTrade; 108 per FindChips (CONFLICT, Newark page not readable) | $4.0700 (OEMsTrade) | 1 (CT); 100 (RL) | not shown | US | https://www.oemstrade.com/search/ft231xq-r, 06:31; https://www.findchips.com/search/FT231XQ-R, 06:29 |
| FT231XQ-R | Mouser | 895-FT231XQ-R | 0 | $2.7700 | not shown | not shown (Mouser page bot-blocked) | US (Mansfield, TX) | https://www.oemstrade.com/search/ft231xq-r, 06:31 |
| FT231XQ-R | TME | FT231XQ-R | "0 in TME stock"; "Hardly available product" | 2.20 USD net | 1 | none given | Poland; ships to US UNVERIFIED | https://www.tme.eu/en/details/ft231xq-r/usb-interfaces-integrated-circuits/ftdi/, 06:29 |
| FT231XS-R | Digi-Key | 768-1129-1-ND (CT) | "In-Stock: 0" | $2.20000 | 1 (CT); TR 2,000 at $1.76250 | "2,000 expected in stock on 16-Mar-2027"; 50 Weeks | US | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XS-R/3029139, 06:42 |
| FT231XS-R | Newark | 83T7089 / 83T7089RL | 0 | $3.8700 | 1 / 100 | not shown | US | https://www.oemstrade.com/search/ft231xs-r, 06:33 |
| FT231XS-R | Mouser | 895-FT231XS-R | 0 | $2.5300 | 1 | not shown | US | https://www.oemstrade.com/search/ft231xs-r, 06:33 |
| FT231XS-R | TME | FT231XS-R | 0 | $2.2200 | 1 | not shown | Poland | https://www.oemstrade.com/search/ft231xs-r, 06:33 |
| FT231XS-U | Mouser | 895-FT231XS-U | 0 | $2.2000 | 1 | not shown | US | https://www.oemstrade.com/search/ft231xs-r, 06:33 |
| FT231XQ-T | Digi-Key | 768-1155-ND (tray) | "In-Stock: 0" | $2.20000 | 1 | "490 expected in stock on 18-Jan-2027"; 50 Weeks | US | https://www.digikey.com/en/products/detail/ftdi-future-technology-devices-international-ltd/FT231XQ-T/3749470, 06:42 |
| FT231XQ-T | Mouser | 895-FT231XQ-T | 0 | $2.2000 | not shown | not shown | US | https://www.oemstrade.com/search/ft231xq-t, 06:33 |
| FT231XQ-T | TME | FT231XQ-T | 0 | $2.2000 | 1 | not shown | Poland | https://www.oemstrade.com/search/ft231xq-t, 06:33 |
| FT231XQ-T | Newark | 15AN6360 | 0 | not listed (1: $4.6500) | 1 | not shown | US | https://www.oemstrade.com/search/ft231xq-t, 06:33 |
| FT231XQ-T | RS | not shown | 0 | price range $2.3800-$2.5900 (FindChips) | not shown | not shown | UK/EU; RS Americas UNVERIFIED | https://www.findchips.com/search/FT231XQ-T, 06:44 |
| FT231XS-U | RS | not shown | 0 | range $2.2000-$2.3900 (FindChips) | not shown | not shown | UK/EU | https://www.findchips.com/search/FT231X, 06:38 |

Note on RS: OEMsTrade listed RS without the authorized badge, but RS is a franchised catalog distributor for many lines; RS's FTDI franchise is UNVERIFIED because FTDI's list could not be read.

## Not authorized (or authorization not shown): brokers and marketplaces

NOT AUTHORIZED unless stated otherwise. Listed for completeness, not as a recommendation. Stock figures are what the aggregators printed and are often broker-pooled or stale.

| Part | Seller | Stock | Price shown | Source, fetched (UTC) |
|------|--------|-------|-------------|----------------------|
| FT231XQ-R | LCSC (C132159) | 22 | 100: $6.0052 (1: $9.3430) | OEMsTrade, 06:31. LCSC's own page gave no stock in fetched text (06:29). LCSC FTDI-authorized: no badge on OEMsTrade; LCSC page claims only "100% Authentic"; authorization UNVERIFIED |
| FT231XQ-R | Win Source Electronics | 11790 (FindChips) / 11890 (OEMsTrade) | $5.5910-$7.1819; 64: $4.6947 | FindChips 06:29, OEMsTrade 06:31 |
| FT231XQ-R | Chip Stock | 24070 | none | FindChips 06:29 |
| FT231XQ-R | Vyrian | 13039 (FindChips) / 2447 (OEMsTrade) | RFQ | FindChips 06:29, OEMsTrade 06:31 |
| FT231XQ-R | Shengyu Electronics (mfr given as "Hongxing Electrical Ltd") | 15345 | none | FindChips 06:29 |
| FT231XQ-R | Chipskey Technology | 33513 | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | Component Stockers | 15000 | 1: $99.9900 | OEMsTrade 06:31 |
| FT231XQ-R | Unikey Electronic | 10000 | 5000: $4.1438 (MOQ 5000) | OEMsTrade 06:31 |
| FT231XQ-R | Time Way Electronics | 10700 | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | Sierra IC | 43601 ("OEM/CM ONLY") | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | New Strength Electronic | 3464 | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | Unicom Electronics | 100 | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | GlobalTek Components | 196; 138; 1200; 124740 (one row says mfr "Texas Instruments") | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | Cytech Systems | 5000 | none | OEMsTrade 06:31 |
| FT231XQ-R | Sense Electronic | 38383 | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | IC Components Limited | 38783 | 1: $6.6999 | OEMsTrade 06:31 |
| FT231XQ-R | Perfect Parts Corporation | 15602; 11477 | RFQ | OEMsTrade 06:31 |
| FT231XQ-R | YIC International | 3000 | $2.7860 all breaks | OEMsTrade 06:31 |
| FT231XQ-R | Neutron USA | 0 | $58.0000 | FindChips 06:29 |
| FT231XS-R | Win Source | 16260 | $3.1310-$4.0219 | FindChips 06:38 |
| FT231XS-R | Bristol Electronics | 78 | none | FindChips 06:38 |
| FT231XS-R | Shengyu | 15101 | none | FindChips 06:38 |
| FT231XS-R | LCSC | 7307 | not read | OEMsTrade 06:33 |
| FT231XS-R | others on OEMsTrade (C Plus 913/246, Hermes 10, Unikey 1612, Chipskey 58846, Time Way 20000, Unicom 147, LIBRA Elektronik 20, Perfect Parts 7544, Silitech 84, GlobalTek 384106/1451/877/349, MountainView 89, Sierra IC 15920, Sense 26984, Vyrian 3852) | as listed | RFQ mostly | OEMsTrade 06:33 |
| FT231XQ-T | Chip Stock 23340; Vyrian 10879; Win Source 11860 ($7.0819-$9.0970); Chip 1 Exchange 5261; Shengyu 5890; ComSIT USA 46 | as listed | as listed | FindChips 06:44 |
| FT231XQ-T | Microchip USA 1439; Chipskey 84135; Unikey 120; PB Signal 50; Sierra IC 1037; New Strength 22865; Cytech 1470; GlobalTek 27438/1015; YIC 1050; Perfect Parts 504 | as listed | RFQ mostly | OEMsTrade 06:33 |

## Counterfeit risk for FTDI parts from brokers

FTDI's USB bridges are among the most counterfeited parts in the trade, and FTDI has twice shipped Windows drivers that act on fakes. In October 2014, Windows driver 2.12.0.0 "silently change[d] the PID" of counterfeit FT232R chips from 0x6001 to 0x0000 in the chip's non-volatile memory, after which no operating system recognized them (SparkFun, 23 Oct 2014, https://news.sparkfun.com/1629, fetched 06:50). In February 2016, a later driver instead injected "NON GENUINE DEVICE FOUND!" into the serial data stream of fake chips (Hackaday, 1 Feb 2016, https://hackaday.com/2016/02/01/ftdi-drivers-break-fake-chips-again/, fetched 06:51). The documented incidents concern FT232R clones; whether FT231X clones exist in volume is UNVERIFIED. The consequence for a data logger is concrete: a board built with a fake bridge can be disabled or corrupted in the field by a routine Windows driver update. Broker stock counts above (tens of thousands of units at sellers with no franchise, one row naming "Texas Instruments" and another "Hongxing Electrical Ltd" as the maker) carry that risk and are not recommended.

## Other routes

- FTDI web shop selling bare ICs: not confirmed. ftdichip.com returned 403 to the fetch tool and a Cloudflare check in Chrome. UNVERIFIED.
- FTDI samples: a 2020-era FTDI page, seen only as a search snippet, says FTDI "can provide IC samples and evaluation kits to anywhere in the world". UNVERIFIED; the current policy needs a direct inquiry to FTDI sales.
- Direct allocation from FTDI: with every catalog house at 0, an email to FTDI's sales office asking for factory stock or allocation of 100-300 FT231XQ-R is the obvious untested route (not contacted, per instructions).

## Best options (authorized sources that could supply 100-300 FT231XQ-R soonest)

1. Newark (83T7088 cut tape, 83T7088RL reel at MOQ 100), US. The only authorized catalog listing with stock reported: 4533 on OEMsTrade (badge "ECIA (NEDA) Member, Authorized Distributor"), 108 on FindChips. Price at 100: $4.0700. The Newark page itself could not be read: check it in a browser first (allow the Chrome extension on newark.com, or open it by hand). Even the low figure covers a pilot.
2. RS (757-0045 cut, 923-1613 reel). Search snippet only: 5,000 units expected to ship from 11 Nov 2026. UNVERIFIED; RS's FTDI franchise also UNVERIFIED. Worth one look at RS Americas.
3. Digi-Key backorder, 768-1128-1-ND: "5,000 expected in stock on 18-Jan-2027", $2.20000 at 100. FT231XQ-T tray (768-1155-ND, same footprint, tray packing) has "490 expected in stock on 18-Jan-2027". A backorder placed now queues for those lots.
4. Mouser (895-FT231XQ-R, $2.7700 at 100), TME ($2.20 at 100), Arrow: all 0 with no restock date read.
5. FTDI sales directly for factory stock or allocation (not contacted).

FT231XS-R (SSOP-20) is no better: 0 at every authorized seller read; Digi-Key "2,000 expected in stock on 16-Mar-2027".
