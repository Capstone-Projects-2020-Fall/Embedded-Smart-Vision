<?php

require_once "config.php";
require_once "session.php";

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['submit'])) {

	$fullname = trim($_POST['name']);
	$email = trim($_POST['email']);
	$password = trim($_POST['password']);
	$confirm_password = trim($_POST["confirm_password"]);
	$password_hash = password_hash($password, PASSWORD_BYCRYPT);

	if($query = $db->prepare("SELECT * FROM users WHERE email = ?")) {
		$error = '';

	$query->bind_param('s', $email);
	$query->execute();
	$query->store_result();

		if ($query->num_rows > 0) {
			$error .= '<p class="error">The email is already registered!</p>';
		} else {
			if (strlen($password ) < 6) {
				$error .= '<p class="error">Passwords must have at least 6 characters.</p>';
			}
			if (empty($confirm_password)) {
				$error .= '<p class="error">Please enter confirm password.</p>';
			} else {
				if (empty($error) && ($password != $confirm_pasword)) {
					$error .= '<p class="error">Password did not match.</p>';
				}
			}
			if (empty($error) ) {
				$insertQuery = $db->prepare("INSERT INTO users (name, email, password) VALUES (?, ?, ?);");
				$insertQuery->bind_param("sss", $fullname, $email, $password_hash);
				$result = $insertQuery->execute();
				if ($result) {
					$error .= '<p class="success">Your account registration was successful!</p>';
				} else {
					$error .= '<p class="error">Something went wrong!</p>';
				}
			}
		}
	}
	$query->close();
	$insertQuery->close();
	mysqli_close($db);
}
?>

<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Sign Up</title>
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
	</head>
	<body>
		<div class="container">
			<div class="row">
				<div class="col-md-12">
					<h2>User Account Registration</h2>
					<p>Please fill this form to create an acount.</p>
					<form action="method=post">
						<div class="form-group">
							<label>Full Name</label>
							<input type="text" name="name" class="form-control" required>
						</div>
						<div class ="form-group">
							<label>Email Address</label>
							<input type="email" name="email" class="form-control" required>
						</div>
						<div class="form-group">
							<label>Password</label>
							<input type="password" name="password" class="form-control" required>
						</div>
						<div class="form-group">
							<label>Confirm Password</label>
							<input type="password" name="confirm_password" class="form-control" required>
						</div>
						<div class="form-group">
							<input type="submit" name="submit" class="btn btn-primary" value="submit">
						</div>
						<p>Already have an account? <a href="login.php">Login here</a>.</p>
					</form>
				</div>
			</div>
		</div>
	</body>
</html>
