import axiosClient from "./axios";


export async function Signup({ email, password, full_name, password2 }) {
    try {
        const response=await axiosClient().post("auth/register_tutor/",
            {
                password,
                username: email,
                full_name,
                email,
                first_name: full_name.split(' ')[0],
                last_name: full_name.replace(full_name.split(' ')[0], ''),
                sessionRate: 4.0,
                image: "",
                user_type: 'tutor',
                bio: 'I am a Tutor!'
            }, {
            headers: {
                Authorization: ''
            }
        });
        if (response.statusCode === 401) {
            return { status: 401, message: response.detail }
        }
        return { data: response.data, status: 200 };
    } catch(errr) {
        console.log(errr)
                return {
            status: 500,
                    message: errr?.response?.data?.error||errr?.response?.data?.message||errr?.response?.data?.detail|| 'Unable To Process Your Request'
        }
    }

}