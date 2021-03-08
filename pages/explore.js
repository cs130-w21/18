import React, {useState} from "react";
import { useRouter } from "next/router";
import {
	fetchExploreMoods,
} from "../lib/fetch";

// by the time the user is allowed to access the explore page, assume they're logged in
export async function getServerSidePropsExplore(context) {
	const cookies = parseCookies(context);

	let username = null,
	  jwt = null;

	username = cookies.username ?? null;
	jwt = cookies.jwt ?? null;
	let data = {},
	error = "";
	if (username && jwt) {
		// request explore moods from backend

		try {
			const exMoodsResponse = await fetchExploreMoods(jwt);
			if (exMoodsResponse.error != "") {
				throw exMoodsResponse.error;
			}
			// extract info we want from response !!
			data.exploreMoods = exMoodsResponse.moods.map((exmood) => ({
				mood_name: exmood.mood_name,
				mood_id: exmood.mood_id,
			}));
		} catch (err) {
			if (err === "Access Token Expired") {
				error = "Your session has expired. Please go to the home page and try again.";
			} else {
				error = "Sorry, we're having trouble accessing moods for you to explore right now. Please try again later."
			}
		}
	}

	return {
		props: {
			data,
			username,
			jwt,
			error,
		}
	}
}

const ExploreController = (props) => {
	const router = useRouter();
	const [error, setError] = useState("");

	const exploreMoods = new Map();
	// convert moods to explore into a map
	if (!error && props.jwt) {
		try {
			props.data.exploreMoods.forEach((exmood) => {
				exploreMoods.set(exmood.mood_id, {
					name: exmood.mood_name,
				});
			});
		} catch {
			setError("Sorry, we're having trouble accessing moods for you to explore. Please try again later."
			);
		}
	}

	const goHome = async () => {
		router.push("/");
	}

	return (
		<>
		  <PageHead />
		  <div className="page_container">
			<HomeButton
			/>
			{props.error !== "" ? (
			  <Alert
				variant="primary"
				className="justify-content-md-center w-50 mx-auto mb-0"
			  >
				{props.error}
			  </Alert>
			) : (
			  ""
			)}
			<div className={styles.big_flex_container}>
			  <div className={`${styles.row} ${styles.row_1}`}>
				<div className={`${styles.intro_box} ${styles.box}`}>
				  {props.username ? `Welcome to the explore page, ${props.username}!` : "Welcome to the explore page!"}
				</div>
				<div className={`${styles.instructions_box} ${styles.box}`}>
				  <p>
					<b>Explore moods created by various users.</b>Save moods using the button on the right.
				  </p>
				</div>
			  </div>
			  <div className={`${styles.row} ${styles.row_2}`}>
				<div
				  className={`${styles.playlists_box} ${styles.box} ${styles.bottom_box}`}
				>
				  <div className={styles.lower_box_text}>Moods To Explore</div>
				  {
					<>
					  <SaveMoodButton savemood={props.savemood} />
					  <div className={styles.list}>{moodListItems}</div>
					</>
				  }
				</div>
				<div className={`${styles.bottom_box} ${styles.box}`}>
				  <div className={styles.lower_box_text}>Save Moods!</div>
				  {saveMoodContents()}
				</div>
			  </div>
			</div>
		  </div>
		</>
	  );
};
		


export default Explore;

