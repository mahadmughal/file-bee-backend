import React from "react";
import { useAuth } from "../contexts/AuthContext";
import { useState, useEffect } from "react";

const Profile = () => {
  const { user, token, updateUser, logOut } = useAuth();
  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || "",
        last_name: user.last_name || "",
        email: user.email || "",
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/api/user/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token.key}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update profile");
      }

      const updatedUser = await response.json();
      setMessage("Profile updated successfully!");
      // Update the user context if necessary
      updateUser({ ...user, ...updatedUser });
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleDeleteAccount = async () => {
    if (
      window.confirm(
        "Are you sure you want to delete your account? This action cannot be undone."
      )
    ) {
      try {
        const response = await fetch(
          "http://localhost:8000/api/user/delete_account",
          {
            method: "DELETE",
            headers: {
              Authorization: `Token ${token.key}`,
            },
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Failed to delete account");
        }

        // Account deleted successfully
        setMessage("Your account has been successfully deleted.");
        // Log out the user and redirect to home page
        logOut();
        // navigate("/sign_in");
      } catch (error) {
        setMessage(`Error: ${error.message}`);
      }
    }
  };

  return (
    <main id="main-container">
      {message && (
        <div className="alert alert-success" role="alert">
          {message}
        </div>
      )}
      <div className="content w-50">
        <div className="block block-rounded block-bordered">
          <div className="block mb-0">
            <div className="block-content block-content-sm block-content-full bg-body">
              <span className="text-uppercase font-size-sm font-w700">
                Personal Information
              </span>
            </div>
            <div className="block-content block-content-full">
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  readOnly
                  className="form-control"
                  id="staticEmail"
                  value={user?.username || ""}
                />
              </div>
              <div className="form-group">
                <label htmlFor="so-profile-name">First Name</label>
                <input
                  type="text"
                  className="form-control"
                  id="first_name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="so-profile-name">Last Name</label>
                <input
                  type="text"
                  className="form-control"
                  id="last_name"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                />
              </div>
            </div>
            <div className="block-content block-content-sm block-content-full bg-body">
              <span className="text-uppercase font-size-sm font-w700">
                Password Update
              </span>
            </div>
            <div className="block-content block-content-full">
              <div className="form-group">
                <label htmlFor="so-profile-password">Current Password</label>
                <input
                  type="password"
                  className="form-control"
                  id="so-profile-password"
                  name="so-profile-password"
                />
              </div>
              <div className="form-group">
                <label htmlFor="so-profile-new-password">New Password</label>
                <input
                  type="password"
                  className="form-control"
                  id="so-profile-new-password"
                  name="so-profile-new-password"
                />
              </div>
              <div className="form-group">
                <label htmlFor="so-profile-new-password-confirm">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="so-profile-new-password-confirm"
                  name="so-profile-new-password-confirm"
                />
              </div>
              <div className="form-group">
                <button type="submit" className="btn btn-primary">
                  Update Password
                </button>
              </div>
            </div>
          </div>
          <div className="block-content block-content-sm block-content-full bg-body">
            <span className="text-uppercase font-size-sm font-w700">
              Delete Account
            </span>
          </div>
          <div className="block-content block-content-full">
            <div className="row p-3">
              Once you delete your account, there is no going back. Please be
              certain.
            </div>
            <div className="row p-3">
              <div className="form-group">
                <button
                  type="submit"
                  className="btn btn-danger"
                  onClick={handleDeleteAccount}
                >
                  <i className="fa fa-fw fa-trash mr-1"></i> Delete your account
                </button>
              </div>
            </div>
          </div>
          <div className="block-content row justify-content-center border-top">
            <div className="col-6 mb-3">
              <button
                type="submit"
                className="btn btn-block btn-hero-primary"
                onClick={handleSubmit}
              >
                <i className="fa fa-fw fa-save mr-1"></i> Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Profile;
