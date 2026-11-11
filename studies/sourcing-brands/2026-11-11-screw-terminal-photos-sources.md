# Screw terminal photo sources

Status: COMPLETE

## Pages tried

- curl of Digi-Key product page: HTTP 403 (blocked); switched to Chrome.
- Digi-Key search ED10567-ND -> https://www.digikey.com/en/products/detail/on-shore-technology-inc/OSTVN10A150/1588870 (OK; page says "Image shown is a representation only", Digi-Key boilerplate).
- Digi-Key VN10A1500000G-ND -> https://www.digikey.com/en/products/detail/amphenol-anytek/VN10A1500000G/4957648: "Photo Not Available" (dead end). Page lists OSTVN10A150 and TBC05-10-1-G-G as parametric equivalents.
- Digi-Key 2073-TBC05-10-1-G-G-ND -> https://www.digikey.com/en/products/detail/gct/TBC05-10-1-G-G/26408888: OK, but the image is the series image MFG_TBC05-02-1-G-G (Digi-Key representation-only boilerplate).
- gct.co/connector/tbc05-10-1-g-g: "Series Not Found" (dead end; curl gets 403; cookie banner declined with Deny).
- https://gct.co/connector/tbc05: OK, one image only, a 3D render. Probed cdn.gct.co TBC05_{1..5}_3D-Render.png: all identical 1000x1000 placeholders (dead end, discarded).
- Digi-Key 277-1281-ND -> https://www.digikey.com/en/products/detail/phoenix-contact/1725737/267470: OK (representation-only boilerplate).
- phoenixcontact.com/en-us/products/pcb-terminal-block-mpt-05-10-254-1725737: Page not found (guessed URL, dead end).
- https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mpt-0510-254-1725737: OK (via site search). One product photo plus drawings; no separate side or wire-entry photo. caas size b1200 returns HTTP 400; b800 is the largest that worked.
- Mouser VN10A1500000G (https://www.mouser.com/c/?q=VN10A1500000G -> product page): placeholder image only (dead end).
- WebSearch 'Amphenol Anytek VN series 2.54mm terminal block VN10A1500000G': distributor pages only.
- RS UK https://uk.rs-online.com/web/p/pluggable-terminal-blocks/0446331 (VN02A1500000G): Access Denied (dead end).
- LCSC https://www.lcsc.com/product-detail/C6325897.html (VN02A1500000G): no product image, placeholder (dead end).
- Newark search VN10A1500000G: no products found (dead end).
- Newark search VN02A1500000G -> https://www.newark.com/amphenol-anytek/vn02a1500000g/tb-wire-to-brd-r-a-2pos-18awg/dp/16AM9720: OK, photo; page says "Image is for illustrative purposes only". Cookie banner left unanswered (no accept). Probed productimages 4565918-41/-42 and 4798098 (VN04A): 404.
- https://www.on-shore.com/product/ostvn10a150/: redirects to an attachment page holding only a STEP model (OSTVN10A150.stp), no photo.
- On Shore site search -> https://www.on-shore.com/part/ostvnxxa150-terminal-block-one-piece-rising-clamp/: OK, one series photo.

## Images saved

- onshore_OSTVN10A150_digikey.jpg, 640x640 JPEG, 10-position, angled view: https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/410/OSTVN10A150.JPG (Digi-Key; representation only)

- gct_TBC05_3pos_render_digikey.jpg, 1920x1920 JPEG: https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/6808/MFG_TBC05-02-1-G-G.jpg (Digi-Key; representation only). File is named for the 2-position part but shows a 3-POSITION block, and it is a CGI render, not a photograph. Shows combination (cross plus slot) screws and 'GCT TBC05 2.54' molded on the end.
- gct_TBC05_render_gct.png, 1920x1920 PNG: https://cdn.gct.co/products/TB/TBC05/TBC05_0_3D-Render.png (GCT's own site; same 3-position CGI render as the Digi-Key image, not a photograph).
- phoenix_1725737_digikey.jpg, 640x640 JPEG, 10-position photograph, wire-entry face: https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/1131/1725737.jpg (Digi-Key; representation only)
- phoenix_1725737_phoenixcontact.png, 800x800 PNG, 10-position, angled: https://caas.phoenixcontact.com/caas/v1/stable/media/1294286/full/b800 (Phoenix Contact; alt text 'Product photo'; looks studio-rendered or heavily retouched; no representation-only label on that page)
- amphenol_VN02A1500000G_newark.jpg, 775x703 JPEG, 2-POSITION photograph (no 10-position photo found), seen from the screw side with the wire entries at the front: https://www.newark.com/productimages/large/en_GB/4565918-40.jpg (Newark/element14; 'for illustrative purposes only')
- onshore_OSTVNXXA150_onshore.jpg, 800x600 JPEG, 6-POSITION photograph (series image, matches OSTVN06A150), angled toward the wire-entry face: https://www.on-shore.com/wp-content/uploads/OSTVNXXA150.jpg (On Shore's own site; no representation-only label)

## Composite

- screw-terminal-photos.png, 1680x1400 PNG, 2x2 grid on white, DejaVu-Sans labels. Tiles: On Shore (Digi-Key 10-pos photo), Amphenol (Newark 2-pos photo), GCT (gct.co 3-pos render), Phoenix (Digi-Key 10-pos photo).

## Visible differences

- On Shore OSTVN: slotted screws sitting near the top surface; seams between positions on the body (modular look); mid green; small step at the end.
- Amphenol Anytek VN (2-pos photo only): pale mint green; slotted screws; two vertical ribs over the pin row on the back.
- GCT TBC05 (render only): yellow-green; combination (cross plus slot) screws; 'GCT TBC05 2.54' and a UR mark molded on the end face; each wire entry framed by a raised rib.
- Phoenix MPT 0,5: darker blue-green in the Digi-Key photo (lighter in Phoenix's own image); screws sunk deep in the bores, head type not resolvable; smooth single-piece body; square clamp openings.
