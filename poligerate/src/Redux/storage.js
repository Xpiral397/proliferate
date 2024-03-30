const KEY_TOKEN_STUDENT = "token_data";
const KEY_TOKEN = "student_data"
const SUCCESS_SIGNUPTOKEN = "APP:USER:DATA";




export const setToken = (token) => {
  localStorage.setItem(KEY_TOKEN, token);
};



export const getToken = () => {
  let token = JSON.parse(localStorage.getItem(KEY_TOKEN_STUDENT) ?? localStorage.getItem(KEY_TOKEN))
  return token?.authentication?.token;
};

