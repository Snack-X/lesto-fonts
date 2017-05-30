var fonts = {
  "Lesto Sans KR": [
    { name: "Black",     weight: 900 },
    { name: "Bold",      weight: 700 },
    { name: "Medium",    weight: 500 },
    { name: "Regular",   weight: 400, default: true },
    { name: "DemiLight", weight: 300 },
    { name: "Light",     weight: 200 },
    { name: "Thin",      weight: 100 },
  ],
  "Lesto Serif KR": [
    { name: "Black",      weight: 900 },
    { name: "Bold",       weight: 700 },
    { name: "SemiBold",   weight: 600 },
    { name: "Medium",     weight: 500 },
    { name: "Regular",    weight: 400, default: true },
    { name: "Light",      weight: 200 },
    { name: "ExtraLight", weight: 100 },
  ],
};

window.addEventListener("load", function() {
  var $selectFont = document.getElementById("select-font");
  var $selectWeight = document.getElementById("select-weight");
  var $textarea = document.getElementById("textarea");

  for(var fontName in fonts) {
    var $option = document.createElement("option");

    $option.innerHTML = fontName;
    $option.setAttribute("value", fontName);

    $selectFont.appendChild($option);
  }

  function onChangeFont() {
    var selectedFont = $selectFont.value;
    $selectWeight.innerHTML = "";
    for(var i = 0 ; i < fonts[selectedFont].length ; i++) {
      var $option = document.createElement("option");

      $option.innerHTML = fonts[selectedFont][i].name;
      $option.setAttribute("value", fonts[selectedFont][i].weight);
      if(fonts[selectedFont][i].default)
        $option.setAttribute("selected", "selected");

      $selectWeight.appendChild($option);
      $textarea.style.fontFamily = selectedFont;
    }
  }

  function onChangeWeight() {
    var selectedWeight = $selectWeight.value;
    $textarea.style.fontWeight = selectedWeight;
  }

  $selectFont.addEventListener("change", onChangeFont);
  $selectWeight.addEventListener("change", onChangeWeight);

  onChangeFont();
  onChangeWeight();
});
