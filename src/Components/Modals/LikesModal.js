import { Modal, Button, ButtonToolbar } from "rsuite";
import React, { useLayoutEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getAuthorId } from "../utils/auth";
import { createReqInstance } from "../utils/axios";

function LIKESMODAL({ postobj, open, handleClose }) {
	const [likes, setLikes] = useState([]);
	var navigate = useNavigate();

	useLayoutEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/signin");
		} else {
			const author_id = getAuthorId(postobj.author.id);
			const post_id = getAuthorId(postobj.id);
			const url = `authors/${author_id}/posts/${post_id}/likes`;
			const reqInstance = createReqInstance(postobj.author.host);
			reqInstance({ method: "get", url: url }).then((res) => {
				setLikes(res.data.items);
			});
		}
	}, []);

	const item = (obj) => {
		return obj.author.displayName;
	};

	return (
		<Modal open={open} onClose={handleClose}>
			<Modal.Header>
				<Modal.Title>Likes on this post</Modal.Title>
			</Modal.Header>
			<Modal.Body>{likes && likes.map((obj) => item(obj))}</Modal.Body>
			<Modal.Footer>
				<Button onClick={handleClose} appearance="primary">
					Ok
				</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default LIKESMODAL;
