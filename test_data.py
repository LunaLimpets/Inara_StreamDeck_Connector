
#TODO TEST HTMLS, Favorite Commodity Cleaned
test_data_trade_routes = [
    [
        ["Navigate"],
        ["Station One", "System One", "Station Distance"],
        ["Station Two", "System Two", "Station Distance"],
        ["Route Distance", "100LS"],
        ["UP NAV"],
        ["Profit Per Hour", "12523"],
        [{"Buy":"Item", "Supply":23523}],
        [{"Sell": "Item", "Demand":123523}],
        ["Profit Per Unit",'123'],
        ["Cancel"],
        ["Updated", "4 Hours ago"],
        [{"Sell":"Item", "Demand":235}],
        [{"Buy":"Item", "Supply":789}],
        ["Profit Per unit", '456'],
        ["Down Nav"]
    ],
    [
        ["Navigate"],
        ["Station One", "System One", "Station Distance"],
        ["Station Two", "System Two", "Station Distance"],
        ["Route Distance", "100LS"],
        ["UP NAV"],
        ["Profit Per Hour", "12523"],
        [{"Buy":"Item", "Supply":23523}],
        [{"Sell": "Item", "Demand":123523}],
        ["Profit Per Unit",'123'],
        ["Cancel"],
        ["Updated", "4 Hours ago"],
        [{"Sell":"Item", "Demand":235}],
        [{"Buy":"Item", "Supply":789}],
        ["Profit Per unit", '456'],
        ["Down Nav"]
    ],
    [
        ["Navigate"],
        ["Station One", "System One", "Station Distance"],
        ["Station Two", "System Two", "Station Distance"],
        ["Route Distance", "100LS"],
        ["UP NAV"],
        ["Profit Per Hour", "12523"],
        [{"Buy":"Item", "Supply":23523}],
        [{"Sell": "Item", "Demand":123523}],
        ["Profit Per Unit",'123'],
        ["Cancel"],
        ["Updated", "4 Hours ago"],
        [{"Sell":"Item", "Demand":235}],
        [{"Buy":"Item", "Supply":789}],
        ["Profit Per unit", '456'],
        ["Down Nav"]
    ]
]

test_raw_data = [{'system': 'LB 3303', 'station': 'Poindexter Horizons', 'type': 'Raw', 'distance': '5.64 Ly', 'stationDistance': '359 Ls'}, {'system': 'L 26-27', 'station': 'McCoy City', 'type': 'Raw', 'distance': '11.35 Ly', 'stationDistance': '412 Ls'}, {'system': 'LHS 3836', 'station': 'Gell-Mann Station', 'type': 'Raw', 'distance': '17.34 Ly', 'stationDistance': '275 Ls'}, {'system': '82 Eridani', 'station': 'Bresnik Port', 'type': 'Raw', 'distance': '17.77 Ly', 'stationDistance': '94 Ls'}, {'system': 'LHS 1339', 'station': 'Bosch City', 'type': 'Raw', 'distance': '18.07 Ly', 'stationDistance': '1,896 Ls'}]
test_manufactured_data = [{'system': 'Quapa', 'station': 'Grabe Dock', 'type': 'Manufactured', 'distance': '31.20 Ly', 'stationDistance': '808 Ls'}, {'system': 'Sirius', 'station': 'Patterson Enterprise', 'type': 'Manufactured', 'distance': '32.07 Ly', 'stationDistance': '1,034 Ls'}, {'system': 'Muth', 'station': 'Gutierrez Hub', 'type': 'Manufactured', 'distance': '32.19 Ly', 'stationDistance': '883 Ls'}, {'system': "Slink's Eye", 'station': 'Kelleam Ring', 'type': 'Manufactured', 'distance': '34.28 Ly', 'stationDistance': '1,056 Ls'}, {'system': 'Tabit', 'station': 'Haber City', 'type': 'Manufactured', 'distance': '37.56 Ly', 'stationDistance': '1,805 Ls'}]
test_encoded_data = [{'system': 'LFT 69', 'station': 'Anning Enterprise', 'type': 'Encoded', 'distance': '14.59 Ly', 'stationDistance': '2,527 Ls'}, {'system': 'Segais', 'station': 'Bates Orbital', 'type': 'Encoded', 'distance': '15.14 Ly', 'stationDistance': '329 Ls'}, {'system': 'Nanabozho', 'station': 'Lamarck Orbital', 'type': 'Encoded', 'distance': '20.44 Ly', 'stationDistance': '2,240 Ls'}, {'system': 'LHS 3295', 'station': 'Yang Hub', 'type': 'Encoded', 'distance': '23.94 Ly', 'stationDistance': '25 Ls'}, {'system': 'LHS 1197', 'station': 'Chretien Terminal', 'type': 'Encoded', 'distance': '24.31 Ly', 'stationDistance': '428 Ls'}]

test_favorite_commodity = {}

tradeRouteHtml = '''<div class="mainblock traderoutebox taggeditem" data-tags='["3"]'><div>From <a href="/elite/station-market/3063/"><span class="standardcase standardcolor nowrap"><div class="stationicon" style="background-image: url(/images/stations/sprites3.png); background-position: -169px 0px;"></div>Veach Hub<wbr> | </wbr></span><span class="uppercase nowrap">Atins</span></a><span class="clipboardbuttonsmall toclipboard" data-clipboard-text="Atins" title="Copy to clipboard"><span class="pictofont">︎</span></span></div><div>To <a href="/elite/station-market/4992/"><span class="standardcase standardcolor nowrap"><div class="stationicon" style="background-image: url(/images/stations/sprites3.png); background-position: -13px 0px;"></div>C
hristian Station<wbr> | </wbr></span><span class="uppercase nowrap">Ross 719</span></a><span class="clipboardbuttonsmall toclipboard" data-clipboard-text="Ross 719" title="Copy to clipboard"><span class="pictofont">︎</span></span></div><div></
div><div><div class="itempaircontainer"><div class="itempairlabel">Station distance</div><div class="itempairvalue"><span class="minor">1,570 Ls</span></div></div></div><div class="traderouteboxtoright"><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Buy</div><div class="itempairvalue"><a href="/elite/commodity/19/"><span class="avoidwrap">Food Cartridges</span></a></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Buy price</div><div class="itempairvalue">102 <span class="minor">Cr</span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Supply</div><div class="itempairvalue">612,310</div></div></div><div class="traderouteboxfromright"><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Sell</div><div class="itempairvalue"><a href="/elite/commodity/46/"><span class="avoidwrap">Silver</span></a></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Sell price</div><div class="itempairvalue">49,033 <span class="minor">Cr</span> <span class="minor">|</span> <span class="major">+15,397 <span class="minor">Cr</span></span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Demand</div><div class="itempairvalue">68,227<div class="supplydemandicon3"><span class="pictofont">︎</span></div></div></div></div><div><div class="itempaircontain
er"><div class="itempairlabel">Station distance</div><div class="itempairvalue"><span class="minor">8 Ls</span></div></div></div><div class="traderouteboxfromleft"><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Sell</div><div class="itempairvalue"><a href="/elite/commodity/19/"><span class="avoidwrap">Food Cartridges</span></a></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Sell price</div><div class="itempairvalue">2,177 <span class="minor">Cr</span> <span class="minor">|</span> <span class="major">+2,075 <span class="minor">Cr</span></span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Demand</div><div class="itempairvalue">19,587<div class="supplydemandicon3"><span class="pictofont">︎</span></div></div></div></div><div class="traderouteboxtoleft"><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Buy</div><div cla
ss="itempairvalue"><a href="/elite/commodity/46/"><span class="avoidwrap">Silver</span></a></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Buy price</div><div class="itempairvalue">33,636 <span class="minor">Cr</span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Supply</div><div class="itempairvalue">1,329<div class="supplydemandicon3"><span class="pictofont">︎</span></div></div></div></div><div>
<div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Route distance</div><div class="itempairvalue itempairvalueright"><span class="bigger">78.82 Ly</span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;">Updated</div><div class="itempairvalue itempairvalueright">2 days ago</div></div></div><div class="traderouteboxprofit" style="margin-top: 5px;"><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;"><span class="tooltip" data-tooltiptext="A profit per unit of a commodity (sell price - buy price = profit)">Profit per unit</span></div><div class="itempairvalue itempairvalueright"><span class="major biggest">17,472</span> <span class="minor">Cr</span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;"><span class="tooltip" data-tooltiptext="A profit per trip (cargo capacity * profit per unit)">Profit per trip</span></div><div class="itempairvalue itempairvalueright">13,138,944 <span class="minor">Cr</span></div></div><div class="itempaircontainer"><div class="itempairlabel" style="width: 80px;"><span class="tooltip" data-tooltiptext="A very rough estimate of a profit per hour, based on a profit per unit, cargo capacity, route distance and station distances.">Profit per hour</span></div><div class="itempairvalue itempairvalueright">48,442,918 <span class="minor">Cr</span></div></div></div></div></div>'''
materialDataHtml = ""
favoriteCommodityHtml = ""