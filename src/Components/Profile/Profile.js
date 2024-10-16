import React, { useEffect, useState } from "react";
import {
	ButtonGroup,
	Panel,
	Button,
	Navbar,
	Nav,
	Input,
	InputGroup,
	Message,
	useToaster,
} from "rsuite";
import FRIENDS from "./Friends";
import AUTHORPOSTS from "./AuthorPosts";
import { useNavigate } from "react-router-dom";
import { reqInstance } from "../utils/axios";
import ADD_FRIEND_MODAL from "../Modals/AddFriendModal";
import {
	getAuthorId,
	getCsrfToken,
	getCurrentUser,
	getProfileImageUrl,
	setCurrentUser,
} from "../utils/auth";
import PROFILEIMAGE from "./ProfileImage";

// this is the profile screen that lets us edit a post
function PROFILE() {
	const [posts, setPosts] = React.useState(true);
	const [appearance, setAppearance] = React.useState({
		posts: "primary",
		friends: "ghost",
	});
	const [author, setAuthor] = useState({});
	let navigate = useNavigate();
	const [open, setOpen] = useState(false);
	const [imageurl, setImage] = useState("");
	const [giturl, setGiturl] = useState("");
	const [count, setCount] = useState(0);
	let toaster = useToaster();

	useEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/signin");
		} else {
			setImage(getProfileImageUrl());
			setAuthor(JSON.parse(localStorage.getItem("user")));
		}
	}, []);

	const handlePostsBtnClick = () => {
		setPosts(true);
		setAppearance({ posts: "primary", friends: "ghost" });
	};

	const handleFriendsBtnClick = () => {
		setPosts(false);
		setAppearance({ posts: "ghost", friends: "primary" });
	};

	const [curPage, setCurPage] = useState("profile");

	const handleInboxClick = () => {
		navigate("/");
	};

	async function handleLogoutClick() {
		reqInstance.post("dlogout/").then((res) => {
			if (res.status === 202) {
				navigate("/signin");
			}
		});
	}

	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author

	const handleOpen = () => {
		setOpen(true);
	};

	const handleModalClose = () => {
		setOpen(false);
	};

	const handleGithubClick = () => {
		if (curPage !== "github") {
			setCurPage("github");
			navigate("/github");
		}
	};

	const handleExploreClick = () => {
		if (curPage !== "explore") {
			setCurPage("explore");
			navigate("/explore");
		}
	};

	const notifySuccessPost = (message) => {
		toaster.push(<Message type="success">{message}</Message>, {
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

	async function handleGitClick() {
		const author_id = getAuthorId(null);
		const url = `authors/${author_id}/`;
		reqInstance({ method: "post", url: url, data: { github: giturl } })
			.then((res) => {
				setCurrentUser(res.data).then(setCount(count + 1));
				notifySuccessPost("successfully upadated the git url");
			})
			.catch((err) => notifyFailedPost(err));
	}

	async function handleImageClick() {
		const author_id = getAuthorId(null);
		const url = `authors/${author_id}/`;
		reqInstance({
			method: "post",
			url: url,
			data: { profileImage: imageurl },
		})
			.then((res) => {
				setCurrentUser(res.data).then(setCount(count + 1));
				notifySuccessPost("successfully upadated the profile url");
			})
			.catch((err) => notifyFailedPost(err.data));
	}

	const header = (
		<div>
			<PROFILEIMAGE size="lg" />
			<h2 style={{ marginLeft: "10px", float: "left" }}>
				{author.displayName}
			</h2>
		</div>
	);

	return (
		<div style={{ padding: "10px", width: "60%", margin: "auto" }}>
			<Navbar>
				<Navbar.Brand>Socially Distrubted</Navbar.Brand>
				<Nav pullRight>
					<Nav.Item onClick={handleLogoutClick}>Logout</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleInboxClick}>Inbox</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleGithubClick}>GitHub</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleExploreClick}>Explore</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item>Profile</Nav.Item>
				</Nav>
				<Nav pullRight>
					<Nav.Item onClick={handleOpen}>Add Friend</Nav.Item>
				</Nav>
			</Navbar>
			<Panel shaded header={header}>
				<InputGroup inside style={{ marginTop: "5px" }}>
					<Input
						placeholder="Profile Image Url"
						value={imageurl}
						default={author.profileImage}
						onChange={(e) => setImage(e)}
					/>
					<InputGroup.Button onClick={handleImageClick}>
						Save
					</InputGroup.Button>
				</InputGroup>

				<InputGroup inside style={{ marginTop: "5px" }}>
					<Input
						placeholder="Github Url"
						value={giturl}
						default={author.github}
						onChange={(e) => setGiturl(e)}
					/>
					<InputGroup.Button onClick={handleGitClick}>
						Save
					</InputGroup.Button>
				</InputGroup>

				<ButtonGroup
					justified
					style={{ paddingTop: "10px", marginBottom: "5px" }}
				>
					<Button
						style={{ textAlign: "center" }}
						appearance={appearance["posts"]}
						onClick={handlePostsBtnClick}
					>
						Posts
					</Button>
					<Button
						style={{ textAlign: "center" }}
						appearance={appearance["friends"]}
						onClick={handleFriendsBtnClick}
					>
						Friends
					</Button>
				</ButtonGroup>
				{posts ? <AUTHORPOSTS /> : <FRIENDS />}
			</Panel>
			<ADD_FRIEND_MODAL open={open} handleClose={handleModalClose} />
		</div>
	);
}

export default PROFILE;
