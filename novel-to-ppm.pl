#!/usr/bin/env perl
# Debug tool: converts a generated Novel txt back to PPM image.
use v5.014;
use warnings;

my %colors = (
  "Air Force blue" => [93,138,168],
  "Alice blue" => [240,248,255],
  "Alizarin crimson" => [227,38,54],
  "Almond" => [239,222,205],
  "Amaranth" => [229,43,80],
  "Amber" => [255,191,0],
  "Amber" => [255,126,0],
  "American rose" => [255,3,62],
  "Amethyst" => [153,102,204],
  "Android Green" => [164,198,57],
  "Anti-flash white" => [242,243,244],
  "Antique brass" => [205,149,117],
  "Antique fuchsia" => [145,92,131],
  "Antique white" => [250,235,215],
  "Ao" => [0,128,0],
  "Apple green" => [141,182,0],
  "Apricot" => [251,206,177],
  "Aqua" => [0,255,255],
  "Aquamarine" => [127,255,212],
  "Army green" => [75,83,32],
  "Arylide yellow" => [233,214,107],
  "Ash grey" => [178,190,181],
  "Asparagus" => [135,169,107],
  "Atomic tangerine" => [255,153,102],
  "Auburn" => [165,42,42],
  "Aureolin" => [253,238,0],
  "AuroMetalSaurus" => [110,127,128],
  "Awesome" => [255,32,82],
  "Azure" => [0,127,255],
  "Azure mist/web" => [240,255,255],
  "Baby blue" => [137,207,240],
  "Baby blue eyes" => [161,202,241],
  "Baby pink" => [244,194,194],
  "Ball Blue" => [33,171,205],
  "Banana Mania" => [250,231,181],
  "Banana yellow" => [255,225,53],
  "Battleship grey" => [132,132,130],
  "Bazaar" => [152,119,123],
  "Beau blue" => [188,212,230],
  "Beaver" => [159,129,112],
  "Beige" => [245,245,220],
  "Bisque" => [255,228,196],
  "Bistre" => [61,43,31],
  "Bittersweet" => [254,111,94],
  "Black" => [0,0,0],
  "Blanched Almond" => [255,235,205],
  "Bleu de France" => [49,140,231],
  "Blizzard Blue" => [172,229,238],
  "Blond" => [250,240,190],
  "Blue" => [0,0,255],
  "Blue" => [0,147,175],
  "Blue" => [0,135,189],
  "Blue" => [51,51,153],
  "Blue" => [2,71,254],
  "Blue Bell" => [162,162,208],
  "Blue Gray" => [102,153,204],
  "Blue-green" => [13,152,186],
  "Blue-violet" => [138,43,226],
  "Blush" => [222,93,131],
  "Bole" => [121,68,59],
  "Bondi blue" => [0,149,182],
  "Boston University Red" => [204,0,0],
  "Boysenberry" => [135,50,96],
  "Brandeis blue" => [0,112,255],
  "Brass" => [181,166,66],
  "Brick red" => [203,65,84],
  "Bright cerulean" => [29,172,214],
  "Bright green" => [102,255,0],
  "Bright lavender" => [191,148,228],
  "Bright maroon" => [195,33,72],
  "Bright pink" => [255,0,127],
  "Bright turquoise" => [8,232,222],
  "Bright ube" => [209,159,232],
  "Brilliant lavender" => [244,187,255],
  "Brilliant rose" => [255,85,163],
  "Brink pink" => [251,96,127],
  "British racing green" => [0,66,37],
  "Bronze" => [205,127,50],
  "Traditional Brown" => [150,75,0],
  "Brown" => [165,42,42],
  "Bubble gum" => [255,193,204],
  "Bubbles" => [231,254,255],
  "Buff" => [240,220,130],
  "Bulgarian rose" => [72,6,7],
  "Burgundy" => [128,0,32],
  "Burlywood" => [222,184,135],
  "Burnt orange" => [204,85,0],
  "Burnt sienna" => [233,116,81],
  "Burnt umber" => [138,51,36],
  "Byzantine" => [189,51,164],
  "Byzantium" => [112,41,99],
  "Cadet" => [83,104,114],
  "Cadet blue" => [95,158,160],
  "Cadet grey" => [145,163,176],
  "Cadmium green" => [0,107,60],
  "Cadmium orange" => [237,135,45],
  "Cadmium red" => [227,0,34],
  "Cadmium yellow" => [255,246,0],
  "Café au lait" => [166,123,91],
  "Café noir" => [75,54,33],
  "Cal Poly Pomona green" => [30,77,43],
  "Cambridge Blue" => [163,193,173],
  "Camel" => [193,154,107],
  "Camouflage green" => [120,134,107],
  "Canary yellow" => [255,239,0],
  "Candy apple red" => [255,8,0],
  "Candy pink" => [228,113,122],
  "Capri" => [0,191,255],
  "Caput mortuum" => [89,39,32],
  "Cardinal" => [196,30,58],
  "Caribbean green" => [0,204,153],
  "Carmine" => [255,0,64],
  "Carmine pink" => [235,76,66],
  "Carmine red" => [255,0,56],
  "Carnation pink" => [255,166,201],
  "Carnelian" => [179,27,27],
  "Carolina blue" => [153,186,221],
  "Carrot orange" => [237,145,33],
  "Celadon" => [172,225,175],
  "Celeste" => [178,255,255],
  "Celestial blue" => [73,151,208],
  "Cerise" => [222,49,99],
  "Cerise pink" => [236,59,131],
  "Cerulean" => [0,123,167],
  "Cerulean blue" => [42,82,190],
  "CG Blue" => [0,122,165],
  "CG Red" => [224,60,49],
  "Chamoisee" => [160,120,90],
  "Champagne" => [250,214,165],
  "Charcoal" => [54,69,79],
  "Traditional Chartreuse" => [223,255,0],
  "Chartreuse" => [127,255,0],
  "Cherry blossom pink" => [255,183,197],
  "Chestnut" => [205,92,92],
  "Traditional Chocolate" => [123,63,0],
  "Chocolate" => [210,105,30],
  "Chrome yellow" => [255,167,0],
  "Cinereous" => [152,129,123],
  "Cinnabar" => [227,66,52],
  "Cinnamon" => [210,105,30],
  "Citrine" => [228,208,10],
  "Classic rose" => [251,204,231],
  "Cobalt" => [0,71,171],
  "Cocoa brown" => [210,105,30],
  "Coffee" => [111,78,55],
  "Columbia blue" => [155,221,255],
  "Cool black" => [0,46,99],
  "Cool grey" => [140,146,172],
  "Copper" => [184,115,51],
  "Copper rose" => [153,102,102],
  "Coquelicot" => [255,56,0],
  "Coral" => [255,127,80],
  "Coral pink" => [248,131,121],
  "Coral red" => [255,64,64],
  "Cordovan" => [137,63,69],
  "Corn" => [251,236,93],
  "Cornell Red" => [179,27,27],
  "Cornflower blue" => [100,149,237],
  "Cornsilk" => [255,248,220],
  "Cosmic latte" => [255,248,231],
  "Cotton candy" => [255,188,217],
  "Cream" => [255,253,208],
  "Crimson" => [220,20,60],
  "Crimson glory" => [190,0,50],
  "Cyan" => [0,255,255],
  "Cyan" => [0,183,235],
  "Daffodil" => [255,255,49],
  "Dandelion" => [240,225,48],
  "Dark blue" => [0,0,139],
  "Dark brown" => [101,67,33],
  "Dark byzantium" => [93,57,84],
  "Dark candy apple red" => [164,0,0],
  "Dark cerulean" => [8,69,126],
  "Dark chestnut" => [152,105,96],
  "Dark coral" => [205,91,69],
  "Dark cyan" => [0,139,139],
  "Dark electric blue" => [83,104,120],
  "Dark goldenrod" => [184,134,11],
  "Dark gray" => [169,169,169],
  "Dark green" => [1,50,32],
  "Dark jungle green" => [26,36,33],
  "Dark khaki" => [189,183,107],
  "Dark lava" => [72,60,50],
  "Dark lavender" => [115,79,150],
  "Dark magenta" => [139,0,139],
  "Dark midnight blue" => [0,51,102],
  "Dark olive green" => [85,107,47],
  "Dark orange" => [255,140,0],
  "Dark orchid" => [153,50,204],
  "Dark pastel blue" => [119,158,203],
  "Dark pastel green" => [3,192,60],
  "Dark pastel purple" => [150,111,214],
  "Dark pastel red" => [194,59,34],
  "Dark pink" => [231,84,128],
  "Dark powder blue" => [0,51,153],
  "Dark raspberry" => [135,38,87],
  "Dark red" => [139,0,0],
  "Dark salmon" => [233,150,122],
  "Dark scarlet" => [86,3,25],
  "Dark sea green" => [143,188,143],
  "Dark sienna" => [60,20,20],
  "Dark slate blue" => [72,61,139],
  "Dark slate gray" => [47,79,79],
  "Dark spring green" => [23,114,69],
  "Dark tan" => [145,129,81],
  "Dark tangerine" => [255,168,18],
  "Dark taupe" => [72,60,50],
  "Dark terra cotta" => [204,78,92],
  "Dark turquoise" => [0,206,209],
  "Dark violet" => [148,0,211],
  "Dartmouth green" => [0,105,62],
  "Davy's grey" => [85,85,85],
  "Debian red" => [215,10,83],
  "Deep carmine" => [169,32,62],
  "Deep carmine pink" => [239,48,56],
  "Deep carrot orange" => [233,105,44],
  "Deep cerise" => [218,50,135],
  "Deep champagne" => [250,214,165],
  "Deep chestnut" => [185,78,72],
  "Deep coffee" => [112,66,65],
  "Deep fuchsia" => [193,84,193],
  "Deep jungle green" => [0,75,73],
  "Deep lilac" => [153,85,187],
  "Deep magenta" => [204,0,204],
  "Deep peach" => [255,203,164],
  "Deep pink" => [255,20,147],
  "Deep saffron" => [255,153,51],
  "Deep sky blue" => [0,191,255],
  "Denim" => [21,96,189],
  "Desert" => [193,154,107],
  "Desert sand" => [237,201,175],
  "Dim gray" => [105,105,105],
  "Dodger blue" => [30,144,255],
  "Dogwood rose" => [215,24,104],
  "Dollar bill" => [133,187,101],
  "Drab" => [150,113,23],
  "Duke blue" => [0,0,156],
  "Earth yellow" => [225,169,95],
  "Ecru" => [194,178,128],
  "Eggplant" => [97,64,81],
  "Eggshell" => [240,234,214],
  "Egyptian blue" => [16,52,166],
  "Electric blue" => [125,249,255],
  "Electric crimson" => [255,0,63],
  "Electric cyan" => [0,255,255],
  "Electric green" => [0,255,0],
  "Electric indigo" => [111,0,255],
  "Electric lavender" => [244,187,255],
  "Electric lime" => [204,255,0],
  "Electric purple" => [191,0,255],
  "Electric ultramarine" => [63,0,255],
  "Electric violet" => [143,0,255],
  "Electric yellow" => [255,255,0],
  "Emerald" => [80,200,120],
  "Eton blue" => [150,200,162],
  "Fallow" => [193,154,107],
  "Falu red" => [128,24,24],
  "Fandango" => [181,51,137],
  "Fashion fuchsia" => [244,0,161],
  "Fawn" => [229,170,112],
  "Feldgrau" => [77,93,83],
  "Fern green" => [79,121,66],
  "Ferrari Red" => [255,40,0],
  "Field drab" => [108,84,30],
  "Firebrick" => [178,34,34],
  "Fire engine red" => [206,32,41],
  "Flame" => [226,88,34],
  "Flamingo pink" => [252,142,172],
  "Flavescent" => [247,233,142],
  "Flax" => [238,220,130],
  "Floral white" => [255,250,240],
  "Fluorescent orange" => [255,191,0],
  "Fluorescent pink" => [255,20,147],
  "Fluorescent yellow" => [204,255,0],
  "Folly" => [255,0,79],
  "Traditional Forest green" => [1,68,33],
  "Forest green" => [34,139,34],
  "French beige" => [166,123,91],
  "French blue" => [0,114,187],
  "French lilac" => [134,96,142],
  "French rose" => [246,74,138],
  "Fuchsia" => [255,0,255],
  "Fuchsia pink" => [255,119,255],
  "Fulvous" => [228,132,0],
  "Fuzzy Wuzzy" => [204,102,102],
  "Gainsboro" => [220,220,220],
  "Gamboge" => [228,155,15],
  "Ghost white" => [248,248,255],
  "Ginger" => [176,101,0],
  "Glaucous" => [96,130,182],
  "Glitter" => [230,232,250],
  "Metallic Gold" => [212,175,55],
  "Gold" => [255,215,0],
  "Golden brown" => [153,101,21],
  "Golden poppy" => [252,194,0],
  "Golden yellow" => [255,223,0],
  "Goldenrod" => [218,165,32],
  "Granny Smith Apple" => [168,228,160],
  "Gray" => [128,128,128],
  "Gray" => [127,127,127],
  "Gray" => [190,190,190],
  "Gray-asparagus" => [70,89,69],
  "Green" => [0,255,0],
  "Green" => [0,128,0],
  "Green" => [0,168,119],
  "Green" => [0,159,107],
  "Green" => [0,165,80],
  "Green" => [102,176,50],
  "Green-yellow" => [173,255,47],
  "Grullo" => [169,154,134],
  "Guppie green" => [0,255,127],
  "Halaya ube" => [102,56,84],
  "Han blue" => [68,108,207],
  "Han purple" => [82,24,250],
  "Hansa yellow" => [233,214,107],
  "Harlequin" => [63,255,0],
  "Harvard crimson" => [201,0,22],
  "Harvest Gold" => [218,145,0],
  "Heart Gold" => [128,128,0],
  "Heliotrope" => [223,115,255],
  "Hollywood cerise" => [244,0,161],
  "Honeydew" => [240,255,240],
  "Hooker's green" => [0,112,0],
  "Hot magenta" => [255,29,206],
  "Hot pink" => [255,105,180],
  "Hunter green" => [53,94,59],
  "Icterine" => [252,247,94],
  "Inchworm" => [178,236,93],
  "India green" => [19,136,8],
  "Indian red" => [205,92,92],
  "Indian yellow" => [227,168,87],
  "Indigo Dye" => [0,65,106],
  "Indigo" => [75,0,130],
  "International Klein Blue" => [0,47,167],
  "International orange" => [255,79,0],
  "Iris" => [90,79,207],
  "Isabelline" => [244,240,236],
  "Islamic green" => [0,144,0],
  "Ivory" => [255,255,240],
  "Jade" => [0,168,107],
  "Jasmine" => [248,222,126],
  "Jasper" => [215,59,62],
  "Jazzberry jam" => [165,11,94],
  "Jonquil" => [250,218,94],
  "June bud" => [189,218,87],
  "Jungle green" => [41,171,135],
  "Kelly green" => [76,187,23],
  "Khaki" => [195,176,145],
  "Light khaki" => [240,230,140],
  "KU Crimson" => [232,0,13],
  "La Salle Green" => [8,120,48],
  "Languid lavender" => [214,202,221],
  "Lapis lazuli" => [38,97,156],
  "Laser Lemon" => [254,254,34],
  "Laurel green" => [169,186,157],
  "Lava" => [207,16,32],
  "Floral Lavender" => [181,126,220],
  "Lavender" => [230,230,250],
  "Lavender blue" => [204,204,255],
  "Lavender blush" => [255,240,245],
  "Lavender gray" => [196,195,208],
  "Lavender indigo" => [148,87,235],
  "Lavender magenta" => [238,130,238],
  "Lavender mist" => [230,230,250],
  "Lavender pink" => [251,174,210],
  "Lavender purple" => [150,123,182],
  "Lavender rose" => [251,160,227],
  "Lawn green" => [124,252,0],
  "Lemon" => [255,247,0],
  "Lemon chiffon" => [255,250,205],
  "Light apricot" => [253,213,177],
  "Light blue" => [173,216,230],
  "Light brown" => [181,101,29],
  "Light carmine pink" => [230,103,113],
  "Light coral" => [240,128,128],
  "Light cornflower blue" => [147,204,234],
  "Light Crimson" => [245,105,145],
  "Light cyan" => [224,255,255],
  "Light fuchsia pink" => [249,132,239],
  "Light goldenrod yellow" => [250,250,210],
  "Light gray" => [211,211,211],
  "Light green" => [144,238,144],
  "Light khaki" => [240,230,140],
  "Light pastel purple" => [177,156,217],
  "Light pink" => [255,182,193],
  "Light salmon" => [255,160,122],
  "Light salmon pink" => [255,153,153],
  "Light sea green" => [32,178,170],
  "Light sky blue" => [135,206,250],
  "Light slate gray" => [119,136,153],
  "Light taupe" => [179,139,109],
  "Light Thulian pink" => [230,143,172],
  "Light yellow" => [255,255,237],
  "Lilac" => [200,162,200],
  "Lime" => [191,255,0],
  "Lime" => [0,255,0],
  "Lime green" => [50,205,50],
  "Lincoln green" => [25,89,5],
  "Linen" => [250,240,230],
  "Lion" => [193,154,107],
  "Liver" => [83,75,79],
  "Lust" => [230,32,32],
  "Magenta" => [255,0,255],
  "Magenta Dye" => [202,31,123],
  "Magenta" => [255,0,144],
  "Magic mint" => [170,240,209],
  "Magnolia" => [248,244,255],
  "Mahogany" => [192,64,0],
  "Maize" => [251,236,93],
  "Majorelle Blue" => [96,80,220],
  "Malachite" => [11,218,81],
  "Manatee" => [151,154,170],
  "Mango Tango" => [255,130,67],
  "Mantis" => [116,195,101],
  "Maroon" => [128,0,0],
  "Maroon" => [176,48,96],
  "Mauve" => [224,176,255],
  "Mauve taupe" => [145,95,109],
  "Mauvelous" => [239,152,170],
  "Maya blue" => [115,194,251],
  "Meat brown" => [229,183,59],
  "Medium aquamarine" => [102,221,170],
  "Medium blue" => [0,0,205],
  "Medium candy apple red" => [226,6,44],
  "Medium carmine" => [175,64,53],
  "Medium champagne" => [243,229,171],
  "Medium electric blue" => [3,80,150],
  "Medium jungle green" => [28,53,45],
  "Medium lavender magenta" => [221,160,221],
  "Medium orchid" => [186,85,211],
  "Medium Persian blue" => [0,103,165],
  "Medium purple" => [147,112,219],
  "Medium red-violet" => [187,51,133],
  "Medium sea green" => [60,179,113],
  "Medium slate blue" => [123,104,238],
  "Medium spring bud" => [201,220,135],
  "Medium spring green" => [0,250,154],
  "Medium taupe" => [103,76,71],
  "Medium teal blue" => [0,84,180],
  "Medium turquoise" => [72,209,204],
  "Medium violet-red" => [199,21,133],
  "Melon" => [253,188,180],
  "Midnight blue" => [25,25,112],
  "Eagle Green" => [0,73,83],
  "Mikado yellow" => [255,196,12],
  "Mint" => [62,180,137],
  "Mint cream" => [245,255,250],
  "Mint green" => [152,255,152],
  "Misty rose" => [255,228,225],
  "Moccasin" => [250,235,215],
  "Mode beige" => [150,113,23],
  "Moonstone blue" => [115,169,194],
  "Mordant red 19" => [174,12,0],
  "Moss green" => [173,223,173],
  "Mountain Meadow" => [48,186,143],
  "Mountbatten pink" => [153,122,141],
  "Mulberry" => [197,75,140],
  "Munsell" => [242,243,244],
  "Mustard" => [255,219,88],
  "Myrtle" => [33,66,30],
  "MSU Green" => [24,69,59],
  "Nadeshiko pink" => [246,173,198],
  "Napier green" => [42,128,0],
  "Naples yellow" => [250,218,94],
  "Navajo white" => [255,222,173],
  "Navy blue" => [0,0,128],
  "Neon Carrot" => [255,163,67],
  "Neon fuchsia" => [254,89,194],
  "Neon green" => [57,255,20],
  "Non-photo blue" => [164,221,237],
  "North Texas Green" => [5,144,51],
  "Ocean Boat Blue" => [0,119,190],
  "Ochre" => [204,119,34],
  "Office green" => [0,128,0],
  "Old gold" => [207,181,59],
  "Old lace" => [253,245,230],
  "Old lavender" => [121,104,120],
  "Old mauve" => [103,49,71],
  "Old rose" => [192,128,129],
  "Olive" => [128,128,0],
  "Olive Drab #3" => [107,142,35],
  "Olive Drab #7" => [60,52,31],
  "Olivine" => [154,185,115],
  "Onyx" => [15,15,15],
  "Opera mauve" => [183,132,167],
  "Orange" => [255,127,0],
  "Orange" => [251,153,2],
  "Orange" => [255,165,0],
  "Orange peel" => [255,159,0],
  "Orange-red" => [255,69,0],
  "Orchid" => [218,112,214],
  "Otter brown" => [101,67,33],
  "Outer Space" => [65,74,76],
  "Outrageous Orange" => [255,110,74],
  "Oxford Blue" => [0,33,71],
  "OU Crimson Red" => [153,0,0],
  "Pakistan green" => [0,102,0],
  "Palatinate blue" => [39,59,226],
  "Palatinate purple" => [104,40,96],
  "Pale aqua" => [188,212,230],
  "Pale blue" => [175,238,238],
  "Pale brown" => [152,118,84],
  "Pale carmine" => [175,64,53],
  "Pale cerulean" => [155,196,226],
  "Pale chestnut" => [221,173,175],
  "Pale copper" => [218,138,103],
  "Pale cornflower blue" => [171,205,239],
  "Pale gold" => [230,190,138],
  "Pale goldenrod" => [238,232,170],
  "Pale green" => [152,251,152],
  "Pale lavender" => [220,208,255],
  "Pale magenta" => [249,132,229],
  "Pale pink" => [250,218,221],
  "Pale plum" => [221,160,221],
  "Pale red-violet" => [219,112,147],
  "Pale robin egg blue" => [150,222,209],
  "Pale silver" => [201,192,187],
  "Pale spring bud" => [236,235,189],
  "Pale taupe" => [188,152,126],
  "Pale violet-red" => [219,112,147],
  "Pansy purple" => [120,24,74],
  "Papaya whip" => [255,239,213],
  "Paris Green" => [80,200,120],
  "Pastel blue" => [174,198,207],
  "Pastel brown" => [131,105,83],
  "Pastel gray" => [207,207,196],
  "Pastel green" => [119,221,119],
  "Pastel magenta" => [244,154,194],
  "Pastel orange" => [255,179,71],
  "Pastel pink" => [255,209,220],
  "Pastel purple" => [179,158,181],
  "Pastel red" => [255,105,97],
  "Pastel violet" => [203,153,201],
  "Pastel yellow" => [253,253,150],
  "Patriarch" => [128,0,128],
  "Payne's grey" => [64,64,79],
  "Peach" => [255,229,180],
  "Peach-orange" => [255,204,153],
  "Peach puff" => [255,218,185],
  "Peach-yellow" => [250,223,173],
  "Pear" => [209,226,49],
  "Pearl" => [234,224,200],
  "Pearl Aqua" => [136,216,192],
  "Peridot" => [230,226,0],
  "Periwinkle" => [204,204,255],
  "Persian blue" => [28,57,187],
  "Persian green" => [0,166,147],
  "Persian indigo" => [50,18,122],
  "Persian orange" => [217,144,88],
  "Persian pink" => [247,127,190],
  "Persian plum" => [112,28,28],
  "Persian red" => [204,51,51],
  "Persian rose" => [254,40,162],
  "Phlox" => [223,0,255],
  "Phthalo blue" => [0,15,137],
  "Phthalo green" => [18,53,36],
  "Piggy pink" => [253,221,230],
  "Pine green" => [1,121,111],
  "Pink" => [255,192,203],
  "Pink-orange" => [255,153,102],
  "Pink pearl" => [231,172,207],
  "Pink Sherbet" => [247,143,167],
  "Pistachio" => [147,197,114],
  "Platinum" => [229,228,226],
  "Traditional Plum" => [142,69,133],
  "Plum" => [221,160,221],
  "Portland Orange" => [255,90,54],
  "Powder blue" => [176,224,230],
  "Princeton orange" => [255,143,0],
  "Prune" => [112,28,28],
  "Prussian blue" => [0,49,83],
  "Psychedelic purple" => [223,0,255],
  "Puce" => [204,136,153],
  "Pumpkin" => [255,117,24],
  "Purple" => [128,0,128],
  "Purple" => [159,0,197],
  "Purple" => [160,32,240],
  "Purple Heart" => [105,53,156],
  "Purple mountain majesty" => [150,120,182],
  "Purple pizzazz" => [254,78,218],
  "Purple taupe" => [80,64,77],
  "Quartz" => [81,72,79],
  "Radical Red" => [255,53,94],
  "Raspberry" => [227,11,93],
  "Raspberry glace" => [145,95,109],
  "Raspberry pink" => [226,80,152],
  "Raspberry rose" => [179,68,108],
  "Raw umber" => [130,102,68],
  "Razzle dazzle rose" => [255,51,204],
  "Razzmatazz" => [227,37,107],
  "Red" => [255,0,0],
  "Red" => [242,0,60],
  "Red" => [196,2,51],
  "Red" => [237,28,36],
  "Red" => [254,39,18],
  "Red-brown" => [165,42,42],
  "Red-violet" => [199,21,133],
  "Redwood" => [171,78,82],
  "Rich black" => [0,64,64],
  "Rich brilliant lavender" => [241,167,254],
  "Rich carmine" => [215,0,64],
  "Rich electric blue" => [8,146,208],
  "Rich lavender" => [167,107,207],
  "Rich lilac" => [182,102,210],
  "Rich maroon" => [176,48,96],
  "Rifle green" => [65,72,51],
  "Robin egg blue" => [0,204,204],
  "Rose" => [255,0,127],
  "Rose bonbon" => [249,66,158],
  "Rose ebony" => [103,72,70],
  "Rose gold" => [183,110,121],
  "Rose madder" => [227,38,54],
  "Rose pink" => [255,102,204],
  "Rose quartz" => [170,152,169],
  "Rose taupe" => [144,93,93],
  "Rose vale" => [171,78,82],
  "Rosewood" => [101,0,11],
  "Rosso corsa" => [212,0,0],
  "Rosy brown" => [188,143,143],
  "Royal azure" => [0,56,168],
  "Traditional Royal blue" => [0,35,102],
  "Royal blue" => [65,105,225],
  "Royal fuchsia" => [202,44,146],
  "Royal purple" => [120,81,169],
  "Ruby" => [224,17,95],
  "Ruddy" => [255,0,40],
  "Ruddy brown" => [187,101,40],
  "Ruddy pink" => [225,142,150],
  "Rufous" => [168,28,7],
  "Russet" => [128,70,27],
  "Rust" => [183,65,14],
  "Sacramento State green" => [0,86,63],
  "Saddle brown" => [139,69,19],
  "Safety orange (blaze orange)" => [255,103,0],
  "Saffron" => [244,196,48],
  "St. Patrick's blue" => [35,41,122],
  "Salmon" => [255,140,105],
  "Salmon pink" => [255,145,164],
  "Sand" => [194,178,128],
  "Sand dune" => [150,113,23],
  "Sandstorm" => [236,213,64],
  "Sandy brown" => [244,164,96],
  "Sandy taupe" => [150,113,23],
  "Sap green" => [80,125,42],
  "Sapphire" => [15,82,186],
  "Satin sheen gold" => [203,161,53],
  "Scarlet" => [255,36,0],
  "Crayola Scarlet" => [255,36,0],
  "School bus yellow" => [255,216,0],
  "Screamin' Green" => [118,255,122],
  "Sea green" => [46,139,87],
  "Seal brown" => [50,20,20],
  "Seashell" => [255,245,238],
  "Selective yellow" => [255,186,0],
  "Sepia" => [112,66,20],
  "Shadow" => [138,121,93],
  "Shamrock green" => [0,158,96],
  "Shocking pink" => [252,15,192],
  "Sienna" => [136,45,23],
  "Silver" => [192,192,192],
  "Sinopia" => [203,65,11],
  "Skobeloff" => [0,116,116],
  "Sky blue" => [135,206,235],
  "Sky magenta" => [207,113,175],
  "Slate blue" => [106,90,205],
  "Slate gray" => [112,128,144],
  "Smalt (Dark powder blue)" => [0,51,153],
  "Smokey topaz" => [147,61,65],
  "Smoky black" => [16,12,8],
  "Snow" => [255,250,250],
  "Spiro Disco Ball" => [15,192,252],
  "Splashed white" => [254,253,255],
  "Spring bud" => [167,252,0],
  "Spring green" => [0,255,127],
  "Steel blue" => [70,130,180],
  "Stil de grain yellow" => [250,218,94],
  "Stizza" => [153,0,0],
  "Straw" => [228,217,111],
  "Sunglow" => [255,204,51],
  "Sunset" => [250,214,165],
  "Tan" => [210,180,140],
  "Tangelo" => [249,77,0],
  "Tangerine" => [242,133,0],
  "Tangerine yellow" => [255,204,0],
  "Taupe" => [72,60,50],
  "Taupe gray" => [139,133,137],
  "Tea green" => [208,240,192],
  "Orange Tea rose" => [248,131,121],
  "Tea rose" => [244,194,194],
  "Teal" => [0,128,128],
  "Teal blue" => [54,117,136],
  "Teal green" => [0,109,91],
  "Tenné (Tawny)" => [205,87,0],
  "Terra cotta" => [226,114,91],
  "Thistle" => [216,191,216],
  "Thulian pink" => [222,111,161],
  "Tickle Me Pink" => [252,137,172],
  "Tiffany Blue" => [10,186,181],
  "Tiger's eye" => [224,141,60],
  "Timberwolf" => [219,215,210],
  "Titanium yellow" => [238,230,0],
  "Tomato" => [255,99,71],
  "Toolbox" => [116,108,192],
  "Topaz" => [255,200,124],
  "Tractor red" => [253,14,53],
  "Trolley Grey" => [128,128,128],
  "Tropical rain forest" => [0,117,94],
  "True Blue" => [0,115,207],
  "Tufts Blue" => [65,125,193],
  "Tumbleweed" => [222,170,136],
  "Turkish rose" => [181,114,129],
  "Turquoise" => [48,213,200],
  "Turquoise blue" => [0,255,239],
  "Turquoise green" => [160,214,180],
  "Tuscan red" => [102,66,77],
  "Twilight lavender" => [138,73,107],
  "Tyrian purple" => [102,2,60],
  "UA blue" => [0,51,170],
  "UA red" => [217,0,76],
  "Ube" => [136,120,195],
  "UCLA Blue" => [83,104,149],
  "UCLA Gold" => [255,179,0],
  "UFO Green" => [60,208,112],
  "Ultramarine" => [18,10,143],
  "Ultramarine blue" => [65,102,245],
  "Ultra pink" => [255,111,255],
  "Umber" => [99,81,71],
  "United Nations blue" => [91,146,229],
  "University of California Gold" => [183,135,39],
  "Unmellow Yellow" => [255,255,102],
  "UP Forest green" => [1,68,33],
  "UP Maroon" => [123,17,19],
  "Upsdell red" => [174,32,41],
  "Urobilin" => [225,173,33],
  "USC Cardinal" => [153,0,0],
  "USC Gold" => [255,204,0],
  "Utah Crimson" => [211,0,63],
  "Vanilla" => [243,229,171],
  "Vegas gold" => [197,179,88],
  "Venetian red" => [200,8,21],
  "Verdigris" => [67,179,174],
  "Vermilion" => [227,66,52],
  "Veronica" => [160,32,240],
  "Violet" => [143,0,255],
  "Violet" => [127,0,255],
  "Violet" => [134,1,175],
  "Violet" => [238,130,238],
  "Viridian" => [64,130,109],
  "Vivid auburn" => [146,39,36],
  "Vivid burgundy" => [159,29,53],
  "Vivid cerise" => [218,29,129],
  "Vivid tangerine" => [255,160,137],
  "Vivid violet" => [159,0,255],
  "Warm black" => [0,66,66],
  "Wenge" => [100,84,82],
  "Wheat" => [245,222,179],
  "White" => [255,255,255],
  "White smoke" => [245,245,245],
  "Wild blue yonder" => [162,173,208],
  "Wild Strawberry" => [255,67,164],
  "Wild Watermelon" => [252,108,133],
  "Wine" => [114,47,55],
  "Wisteria" => [201,160,220],
  "Xanadu" => [115,134,120],
  "Yale Blue" => [15,77,146],
  "Yellow" => [255,255,0],
  "Yellow" => [239,204,0],
  "Yellow" => [255,211,0],
  "Yellow" => [255,239,0],
  "Yellow" => [254,254,51],
  "Yellow-green" => [154,205,50],
  "Yellow Orange" => [255,174,66],
  "Zaffre" => [0,20,168],
  "Zinnwaldite brown" => [44,22,8],
);

# Open file for reading
if (open my $fh,'<',$ARGV[0)
{
  # track x-resolution of image
  my $xres;
  # ppm rows
  my @rows;

  while (<$fh>)
  {
    next if ($_ !~ m/\. /);	# skip non-sentence lines
    chomp;			# remove newline

    # split into sentences, record x-resolution too
    my @sentences = split /\. /;
    $xres = @sentences;

    # Strip alpha-channel info from sentences
    map { $_ =~ s/,.*$//g } @sentences;

    # magic: convert each sentence to space-separated RGB triad,
    #  put all triads together with tabs,
    #  and push onto the end of the rows array.
    push @rows, join "\t", map { join ' ', @{$colors{$_}} } @sentences;
  }

  # dump ppm
  say "P3";
  say "$xres " . @rows;
  say "255";
  map { say $_ } @rows;
} else {
  die "can't open $ARGV[0]: $!\n";
}
