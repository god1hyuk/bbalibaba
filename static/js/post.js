function uploadItemImg(input) {
    // const url = document.querySelector('#item-img').value;
    const imgbox = document.querySelector('#uploaded-img');
    const img = document.createElement('img');

    const reader = new FileReader();
    reader.onload = ({target}) => {
        img.src = target.result;
        console.log(img.src)
    };
    reader.readAsDataURL(input.files[0]);
    imgbox.append(img);
}