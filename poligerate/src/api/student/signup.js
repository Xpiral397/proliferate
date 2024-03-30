import axiosClient from "../axios";


export async function SignupUser({email, password, first_name, password2, username, last_name}) {
    try {
        const response=await axiosClient().post("auth/register_student/",
            {
                username,
                password,
                user_type:'student',
                last_name,
                email,
                first_name,
                image: "",
                bio: 'I am a Student!'
            }, {
            headers: {
                Authorization: ''
            }
        });
        if(response.statusCode===401) {
            return {status: 401, message: response.detail}
        }
        return {data: response.data, status: 201};
    } catch(errr) {
        return {
            status: 500,
            message: errr?.response?.data?.error||errr?.response?.data?.message||errr?.response?.data?.detail||'Unable To Process Your Request'
        }
    }

}