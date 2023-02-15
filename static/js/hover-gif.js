document
  .getElementById("profile-pic")
  .addEventListener("mouseover", showJobDescription);

function showJobDescription() {
  var trailimage = ["static/pic/cat.gif", 375, 255];
  var offsetfrommouse = [20, -25];
  var displayduration = 0;

  var img = document.createElement("img");
  img.src = trailimage[0];
  img.style.position = "absolute";
  img.style.visibility = "visible";
  img.style.left = "0px";
  img.style.top = "0px";
  img.style.width = trailimage[1] + "px";
  img.style.height = trailimage[2] + "px";

  document.body.appendChild(img);

  function gettrailobj() {
    return img.style;
  }

  function truebody() {
    return !window.opera &&
      document.compatMode &&
      document.compatMode != "BackCompat"
      ? document.documentElement
      : document.body;
  }

  function hidetrail() {
    gettrailobj().visibility = "hidden";
    document.onmousemove = "";
  }

  function followmouse(e) {
    var xcoord = offsetfrommouse[0];
    var ycoord = offsetfrommouse[1];
    if (typeof e != "undefined") {
      xcoord += e.pageX;
      ycoord += e.pageY;
    } else if (typeof window.event != "undefined") {
      xcoord += truebody().scrollLeft + event.clientX;
      ycoord += truebody().scrollTop + event.clientY;
    }
    var docwidth = document.all
      ? truebody().scrollLeft + truebody().clientWidth
      : pageXOffset + window.innerWidth - 15;
    var docheight = document.all
      ? Math.max(truebody().scrollHeight, truebody().clientHeight)
      : Math.max(document.body.offsetHeight, window.innerHeight);
    if (
      xcoord + trailimage[1] + 3 > docwidth ||
      ycoord + trailimage[2] > docheight
    )
      gettrailobj().display = "none";
    else gettrailobj().display = "";
    gettrailobj().left = xcoord + "px";
    gettrailobj().top = ycoord + "px";
  }

  document.onmousemove = followmouse;
  document.onmouseout = hidetrail;

  if (displayduration > 0) setTimeout("hidetrail()", displayduration * 1000);
}
