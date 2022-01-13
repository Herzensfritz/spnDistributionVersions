/**
* selectVersion.js: select an angular distribution version.
*
* author: Christian Steiner
* email: christian.steiner@unibas.ch
* license: GPL v3
*
*    Copyright (C) University of Basel 2021  
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with this program.  If not, see <https://www.gnu.org/licenses/> 
**/

/**
 * Script adds a selection that allows the user to select a specific angular distribution folder.
 * Based on the selection (or the current URL), the script loads the relevant scripts from the selected angular folder.
 * Reads a json-file 'versions.json' that describes the distribution versions.
 * (The json-file can be created with the python script 'addVersion.py'.)
 **/
$(document).ready(function(){
   var currentUrl = new URL(location.href);
   $("body").prepend("<div id=\"selectContainer\" class=\"mui-select\"><select id=\"selectVersion\"></select></div>");
   $.getJSON("/versions.json", function(versions){
      if (versions.length == 1){
         $("body").remove("#selectVersion");
         $("selectContainer").append("<select id=\"selectVersion\" disabled=\"true\"></select>");
      } 
      var currentVersion = writeBase(currentUrl, versions[0].number, versions.map(version =>version.number));
      $("body").append("<app-root><\/app-root>");
      versions.forEach(version =>{
         writeOptions(version, currentVersion);    
         writeScripts(version.scripts);
      });
   }).fail(function(){
      console.log("Could not read 'versions.json'!");
   });
   // Poll for fullscreen toggle change
   var fullscreen = false;
   setInterval(function(){
       if(location.href.includes('fullscreen=true') && !fullscreen){
            fullscreen = true;         
            $("#selectContainer").hide();
       } else if (location.href.includes('fullscreen=false') && fullscreen){
            fullscreen = false;         
            $("#selectContainer").show();
       }
   },500);
   // Act on selection changes -> change location to new version.
   $("#selectVersion").change(function(){
      var version = $(this).find("option:selected").attr("value");
      currentUrl = new URL(location.href);
      location.href = "/" + version + "/" + currentUrl.pathname.split('/').slice(2).join('/') + "?" + currentUrl.searchParams.toString();
   });
});
/**
 * Write the current base to the document body and return its value.
 **/
function writeBase(currentUrl, newestVersion, versionNumbers){
  var baseHref = currentUrl.pathname.split('/')[1];
  if (baseHref == '' || !versionNumbers.includes(baseHref)){
      baseHref = newestVersion;
  }
  $("head").append("<base href=\"/" + baseHref + "/\"/>");
  return baseHref;
}
/**
 * Write the options of the version selection to #selectVersion.
 **/
function writeOptions(version, currentVersion){
   if(version.number == currentVersion){
      $("#selectVersion").append("<option selected=\"selected\" value=\"" + version.number +"\">" + version.name + " " + version.number + "</option>");
   } else {
      $("#selectVersion").append("<option value=\"" + version.number +"\">" + version.name + " " + version.number + "</option>");
   }
}
/**
 * Write the scripts that should be loaded to the document body.
 **/
function writeScripts(scripts){
   scripts.forEach(script =>{
      if(script.isModule){
         $("body").append("<script src=\"" + script.src + "\" type=\"module\"><\/script>");
      } else {
         $("body").append("<script src=\"" + script.src + "\" nomodule defer><\/script>");
      }
   });
}
