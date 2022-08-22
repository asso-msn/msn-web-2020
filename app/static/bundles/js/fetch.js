async function fetch_json(url, data={}) {
	let method = "GET";
	if (Object.keys(data))
		method = "POST";
	const response = await fetch(url, {
		method: method,
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(data)
	});
	return response;
}
