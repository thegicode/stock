var myHeaders = new Headers();
myHeaders.append("content-type", "application/json");
myHeaders.append("authorization", "Bearer ");
myHeaders.append("appkey", "");
myHeaders.append("appsecret", "");
myHeaders.append("tr_id", "FHKST01010100");

var raw = "";

var requestOptions = {
  method: 'GET',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price?fid_cond_mrkt_div_code=J&fid_input_iscd=005930", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));