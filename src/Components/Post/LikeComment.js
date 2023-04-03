import React, { useState, useEffect } from "react";
import { IconButton, useToaster, Message } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import { reqInstance } from "../utils/axios";
import { getAuthorId, getCurrentUser } from "../utils/auth";

// Component Imports
function COMMENTLIKE({ obj }) {
	// const [like, set_like] = useState(likeobj);
	const [new_like, set_new_like] = useState("");
	const toaster = useToaster();

	//Confirm the name of the button
	async function handleSubmitClick() {
		const author = JSON.parse(localStorage.getItem("user"));
		var FAID = "";
		const url2 = obj;

		await reqInstance({ method: "get", url: url2 + "/" }).then((res) => {
			FAID = getAuthorId(res.data.author.id);
		});

		const params = {
			type: "Like",
			author: author,
			object: url2,
		};
		const url = `authors/${FAID}/inbox/`;
		//Confirm what to add into the params and send inbox
		reqInstance({ method: "post", url: url, data: params })
			.then((res) => {
				if (res.status == 200) {
					toaster.push(
						<Message type="success">Successful Like</Message>,
						{
							placement: "topEnd",
							duration: 5000,
						}
					);
				} else if (res.status == 400) {
					toaster.push(
						<Message type="error">
							You already liked this post
						</Message>,
						{
							placement: "topEnd",
							duration: 5000,
						}
					);
				}
			})
			.catch((err) => {
				toaster.push(<Message type="error">{err}</Message>, {
					placement: "topEnd",
					duration: 5000,
				});
			});
	}

	return (
		<IconButton
			style={{ float: "right", marginRight: "10px" }}
			appearance="subtle"
			icon={<ThumbsUpIcon />}
			size="xs"
			onClick={handleSubmitClick}
		/>
	);
}

export default COMMENTLIKE;
