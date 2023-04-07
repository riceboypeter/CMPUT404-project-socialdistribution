import React, { useEffect, useLayoutEffect, useState } from "react";
import { Panel, PanelGroup } from "rsuite";
import COMMENTS from "../Post/Comment";
import { reqInstance } from "../utils/axios";
import { useParams } from "react-router-dom";
import POST from "../Post/Post";
import EditIcon from "@rsuite/icons/Edit";
import TrashIcon from "@rsuite/icons/Trash";
import { getAuthorId } from "../utils/auth";
import { useNavigate } from "react-router-dom";

// this shows all the posts in the profile screen
function AUTHORPOSTS() {
	const [posts, setPosts] = useState([]);
	let navigate = useNavigate();

	useEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/signin");
		} else {
			const author_id = getAuthorId(null);
			const url = `authors/${author_id}/posts/`;
			reqInstance({ method: "get", url: url })
				.then((res) => {
					setPosts(res.data.items);
				})
				.catch((err) => console.log(err));
		}
	}, []);

	const body = (obj) => {
		if (obj["contentType"] === "text/plain") {
			return <p style={{ padding: "5px" }}>{obj["content"]}</p>;
		}

		// Peter you just need to return the image here
		if (obj["contentType"] === "image/jpeg") {
			return <div>image</div>;
		}
	};

	const item = (obj) => {
		return (
			<Panel
				key={obj.id}
				header={<div>{obj["title"]}</div>}
				style={{
					marginTop: "5px",
				}}
				bordered
				collapsible
			>
				<POST
					postobj={obj}
					edit={true}
					explore={true}
					github={false}
				></POST>
			</Panel>
		);
	};

	return <PanelGroup>{posts.map((obj) => item(obj))}</PanelGroup>;
}

export default AUTHORPOSTS;
