function myFunction(id) {
    var dropdownContents = document.getElementsByClassName("dropdown-content show");
    var i;
    for(i = 0; i < dropdownContents.length; i++) {
      var dropdownContent = dropdownContents[i];
      if (dropdownContent.classList.contains('show') && dropdownContent.id != 'myDropdown-'+id) {
        console.log("hi");
        dropdownContent.classList.remove('show')
      }
    }
    console.log("hi1");
    document.getElementById("myDropdown-"+id).classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
}

function popupFunction(id){
  document.getElementById('open-popup-'+id).addEventListener('click', function(event) {
    document.getElementById('popup-overlay').style.display = 'block';
  });
  
  
}

document.getElementById('close-popup').addEventListener('click', function() {
  document.getElementById('popup-overlay').style.display = 'none';
});


document.addEventListener('DOMContentLoaded', function () {
  const coll = document.querySelectorAll('.collapsible');
  coll.forEach(item => {
      item.addEventListener('click', function () {
          this.classList.toggle('active');
          const content = this.nextElementSibling;
          content.classList.toggle('show');
      });
  });
});

function extendItems(id) {
  rows = document.getElementsByName('content-'+id);

  for (var i = 0; i < rows.length; i++) {
    rows[i].classList.toggle('show')
  }

}
