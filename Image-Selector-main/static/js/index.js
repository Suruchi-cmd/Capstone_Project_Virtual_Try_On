const bigImageContainers = document.getElementsByClassName(
  "big-image-container"
);

const loadingOverlayElement = document.getElementById(
  "overlay"
);
let isLoading = false;
function updateLoadingOverlay(isLoading=isLoading){
  loadingOverlayElement.className = isLoading ? "overlay" : ""
}


function selectImage(imageSrc, index = 0) {
  const activeContainer = bigImageContainers[index];
  const selectedImage = document.createElement("img");

  selectedImage.className = `big-image big-image-${index}`;
  selectedImage.src = imageSrc;
  activeContainer.innerHTML = "";
  activeContainer.appendChild(selectedImage);
}

function convertImage() {
  const image1 = document.getElementsByClassName("big-image-0")[0];
  const image2 = document.getElementsByClassName("big-image-1")[0];
  if (!image1 || !image2) {
    alert("Please select both the images!");
    return;
  }
  if (image1.src === image2.src) {
    alert("Please select different images!");
    return;
  }
  apiCall();
}

async function postRequest(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

function apiCall() {
  isLoading=true;
  updateLoadingOverlay(isLoading);


  // do YOur operation here!!!
  const image1 = document.getElementsByClassName("big-image-0")[0];
  const image2 = document.getElementsByClassName("big-image-1")[0];

  // Extract filenames from the src attribute of images
  const filename1 = image1.src.split('/').pop();
  const filename2 = image2.src.split('/').pop();

  console.log("Selected Image Filenames:", filename1, filename2);
  // Prepare the data to be sent in the POST request
  const postData = {
    filename1: filename1,
    filename2: filename2
  };
  const url = '/convert';
  // Make the POST request using fetch
  postRequest(url,postData)
  .then(data => {
    console.log(data);
    window.open('/result',target = '_blank')
    isLoading=false;
    updateLoadingOverlay(isLoading);
  })

  
}
