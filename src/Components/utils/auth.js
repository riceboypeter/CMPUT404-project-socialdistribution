import axios from "axios";

// Sets the authorization token
export const setAxiosAuthToken = (token) => {
	if (typeof token !== "undefined" && token) {
		//Apply the TOKEN for every request that we will make in the future.
		axios.defaults.headers.common["Authorization"] = "Token " + token;
	} else {
		//Delete auth header
		delete axios.defaults.headers.common["Authorization"];
	}
};

// cookie to check if a user is logged in
export const setLoggedIn = (bool) => {
	localStorage.setItem("loggedIn", bool);
};
// sets up the csrf token
export const setToken = (token) => {
	localStorage.setItem("token", token);
};
// sets the cookie for the  user info
export async function setCurrentUser(user) {
	return localStorage.setItem("user", JSON.stringify(user));
}
// clears cookies when a user logs out
export const unsetCurrentUser = () => {
	setAxiosAuthToken(null);
	localStorage.removeItem("token");
	localStorage.removeItem("user");
	localStorage.removeItem("loggedIn");
};
// gets the current user from the database and sets the cookie
export async function getCurrentUser(author_id) {
	if (!localStorage.getItem("user")) {
		return await axios({
			method: "get",
			url: `authors/${author_id}`,
			baseURL: `${process.env.REACT_APP_HOST_NAME}/`,
		})
			.then((response) => {
				const user = response.data;
				setCurrentUser(user);
			})
			.catch((res) => console.log(res));
	} else {
		return localStorage.getItem("user");
	}
}
// requests a csrf token from the server and sets the cookie
export async function getCsrfToken() {
	let _csrfToken = null;
	const API_HOST = process.env.REACT_APP_HOST_NAME;
	if (_csrfToken === null) {
		const response = await fetch(`${API_HOST}/csrf/`, {
			credentials: "include",
		});
		const data = await response.json();
		_csrfToken = data.csrfToken;
	}
	setToken(_csrfToken);
	return _csrfToken;
}
// given a url id, it extracts the authors id out of it
export function getAuthorId(a_id) {
	let author_id = "";
	const len = 36;

	if (a_id === null) {
		const author = JSON.parse(localStorage.getItem("user"));

		let arr = author.id;

		if (arr.endsWith("/")) {
			arr = arr.slice(0, -1);
		}
		arr = arr.split("/");
		author_id = arr[arr.length - 1];
	} else {
		if (a_id.endsWith("/")) {
			a_id = a_id.slice(0, -1);
		}
		let arr = a_id.split("/");
		author_id = arr[arr.length - 1];
	}
	return author_id;
}
// gets the profile image of the user
export const getProfileImageUrl = () => {
	const user = JSON.parse(localStorage.getItem("user"));
	if (localStorage.getItem("loggedIn")) {
		return user.profileImage;
	}
};
// sets the username and password cookies
export const setCreds = (obj) => {
	localStorage.setItem("username", obj.username);
	localStorage.setItem("password", obj.password);
};
