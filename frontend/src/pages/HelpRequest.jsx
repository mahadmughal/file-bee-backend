import React, { useState } from "react";
import { useAuth } from "../contexts/AuthContext";
import { useApiService } from "../services/apiService";
import { useNavigate } from "react-router-dom";

const HelpRequest = () => {
  const { user } = useAuth();
  const apiService = useApiService();
  const [message, setMessage] = useState("");
  const [formData, setFormData] = useState({
    email: user?.email || "",
    subject: "",
    description: "",
    attachment: null,
  });
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value, files } = e.target;
    if (name === "attachment") {
      setFormData((prevState) => ({
        ...prevState,
        [name]: files[0],
      }));
    } else {
      setFormData((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log(formData);

      const response = await apiService.submitHelpRequest(formData);

      console.log("response: ", response);
      setMessage("Help request submitted successfully!");
      navigate("/help");
    } catch (error) {
      setMessage(
        `Error: ${error.response?.data?.message || "Failed to submit request"}`
      );
    }
  };

  return (
    <main id="main-container">
      {message && (
        <div
          className={`alert ${
            message.includes("Error") ? "alert-danger" : "alert-success"
          }`}
          role="alert"
        >
          {message}
        </div>
      )}
      <div className="content w-50">
        <div className="block block-rounded block-bordered">
          <div className="block mb-0">
            <div className="block-content block-content-sm block-content-full bg-body">
              <span className="text-uppercase font-size-sm font-w700">
                Submit request
              </span>
            </div>
            <div className="block-content block-content-full">
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="email">Email address</label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="subject">Subject</label>
                  <input
                    type="text"
                    className="form-control"
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea
                    className="form-control"
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    required
                  />
                  <small>
                    Please enter the details of your request. A member of our
                    support team will respond as soon as possible.
                  </small>
                </div>
                <div className="form-group">
                  <label htmlFor="attachment">Attachment</label>
                  <div class="custom-file">
                    <input
                      type="file"
                      class="custom-file-input"
                      data-toggle="custom-file-input"
                      id="attachment"
                      name="attachment"
                      onChange={handleInputChange}
                    />
                    <label class="custom-file-label" for="attachment">
                      {formData.attachment?.name || "Choose file"}
                    </label>
                  </div>
                </div>
                <div className="block-content row justify-content-center border-top">
                  <div className="col-6 mb-1">
                    <button
                      type="submit"
                      className="btn btn-block btn-hero-primary"
                    >
                      <i className="fa fa-fw fa-save mr-1"></i> Submit
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default HelpRequest;
