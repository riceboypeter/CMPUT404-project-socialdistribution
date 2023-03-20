import React, { useState } from "react";
import {
	Input,
	Avatar,
	useToaster,
	Message,
	Dropdown,
	Uploader,
	Button,
} from "rsuite";
import axios from "axios";
import "react-toastify/dist/ReactToastify.css";
import FileBase4 from 'react-file-base64';
import { getAuthorId } from "../utils/auth";

function CREATEPOST() {
	const [post_status, set_post_status] = useState("Public");
	const [post_type, set_post_type] = useState("text/plain");
	const [text, setText] = useState("");
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");
	const [categories, setCategories] = useState("");
	const [markdown, setMarkdown] = useState("");
	const toaster = useToaster();

	const input = () => {
		if (post_type === "text/plain") {
			return (
				<div>
					<Input
						style={{
							float: "left",
							marginTop: "5px",
							marginBottom: "5px",
						}}
						as="textarea"
						rows={5}
						placeholder="Text"
						value={text}
						onChange={(e) => setText(e)}
					/>
				</div>
			);
		}

		if (post_type === "text/markdown") {
			return (
				<div>
					<Input
						style={{
							float: "left",
							marginTop: "5px",
							marginBottom: "5px",
						}}
						as="textarea"
						rows={5}
						placeholder="Text"
						value={text}
						onChange={(e) => setText(e)}
					/>
				</div>
			);
		}

		// should convert image to base64 before posting here
		if (post_type === "Image") {
			return (
				<div>
					<Uploader
						action="post/authors/{AUTHOR_ID}/posts/"
						accept=".png, .jpg"
						autoUpload={false}
						draggable
						style={{
							float: "left",
							width: "100%",
							margin: "auto",
							paddingTop: "5px",
						}}
					>
						<div
							style={{
								height: "100px",
								display: "flex",
								alignItems: "center",
								justifyContent: "center",
							}}
						>
							<span>
								Click or Drag files to this area to upload
							</span>
						</div>
					</Uploader>
				</div>
			);
		}
	};

	const notifySuccessPost = () => {
		toaster.push(<Message type="success">Successful post</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const handlePostClick = () => {
		const author = JSON.parse(localStorage.getItem("user"));
		const author_id = getAuthorId(null);
		const url = `posts/authors/${author_id}/posts/`;
		var params = {
			title: title,
			description: description,
			content: text,
			contentType: post_type,
			visiblity: post_status,
			categories: categories,
			count: 0,
		};
		axios({ method: "post", url: url, data: params })
			.then((res) => {
				if (res.status === 200) {
					notifySuccessPost();
					setText("");
					setDescription("");
					setTitle("");
					setCategories("");
					set_post_status("Public");
					set_post_type("text/plain");
					setMarkdown("");
				} else {
					notifyFailedPost(res.data);
				}
			})
			.catch((err) => console.log(err));
	};

	return (
		<div
			style={{
				marginBottom: "5px",
				height: "auto",
				border: "1px solid black",
				borderRadius: "10px",
				padding: "5px",
				position: "relative",
			}}
		>
			<Avatar
				style={{ float: "left" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			/>
			<Dropdown
				title={post_status}
				activeKey={post_status}
				onSelect={(eventkey) => set_post_status(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="Public">Public</Dropdown.Item>
				<Dropdown.Item eventKey="Friends">Friends</Dropdown.Item>
				<Dropdown.Item eventKey="Private">Private</Dropdown.Item>
			</Dropdown>
			<Dropdown
				title={post_type}
				activeKey={post_type}
				onSelect={(eventkey) => set_post_type(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="text/plain">Plain</Dropdown.Item>
				<Dropdown.Item eventKey="text/markdown">Markdown</Dropdown.Item>
				<Dropdown.Item eventKey="image/png">Png</Dropdown.Item>
				<Dropdown.Item eventKey="image/jpeg">Jpeg</Dropdown.Item>
			</Dropdown>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="Categories"
				value={categories}
				onChange={(e) => setCategories(e)}
			/>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="Title"
				value={title}
				onChange={(e) => setTitle(e)}
			/>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="description"
				value={description}
				onChange={(e) => setDescription(e)}
			/>
			{input()}
			<Button
				style={{ marginTop: "3px" }}
				onClick={handlePostClick}
				appearance="primary"
				block
			>
				Post
			</Button>
		</div>
	);
}

export default CREATEPOST;
