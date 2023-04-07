import React, { useState, useEffect } from "react";
import { IconButton, useToaster, Message } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import { reqInstance, createReqInstance } from "../utils/axios";
import { getAuthorId } from "../utils/auth";

// Component Imports
function LIKE({ postObj }) {
	// const [like, set_like] = useState(likeobj);
	const [new_like, set_new_like] = useState("");
	const toaster = useToaster();
	const postObjUrl = postObj.source;
	// const [users, setusers] = useState([]);
	//Confirm the name of the button
	const handleSubmitClick = () => {
		const FAID = getAuthorId(postObj.author["id"]);
		const author_id = getAuthorId(null);
		const host = postObj.author["host"];
		// const host = "http://127.0.0.1:8000/"
		// http://127.0.0.1:8000
		const user = JSON.parse(localStorage.getItem("user"));
		delete user.type;
		// const user = JSON.parse(localStorage.getItem("user"));
		const params = {
			type: "Like",
			author: user,
			object: postObjUrl,
		};
		const url = `authors/${FAID}/inbox/`;
		const reqInstance = createReqInstance(host); // Create axios instance with default base URL
		// reqInstance.post({ url: url, baseurl: host, data: params })
		reqInstance
			.post(url, params)
			.then((res) => {
				toaster.push(
					<Message type="success">Successful Like</Message>,
					{
						placement: "topEnd",
						duration: 5000,
					}
				);
			})
			.catch((err) => {
				toaster.push(<Message type="error">{err}</Message>, {
					placement: "topEnd",
					duration: 5000,
				});
			});
	};

	return (
		<IconButton
			style={{ float: "right", marginRight: "10px" }}
			appearance="subtle"
			icon={<ThumbsUpIcon />}
			onClick={handleSubmitClick}
		/>
	);
}

export default LIKE;
