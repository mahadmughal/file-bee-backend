import React from "react";

function Features() {
  return (
    <div id="dm-features" className="bg-white px-8">
      <div className="content content-full">
        <div className="row py-3">
          <div className="col-sm-6 col-md-4 mb-5">
            <div className="my-3">
              <i className="fa fa-2x fa-desktop text-primary"></i>
            </div>
            <h4 className="h5 mb-2">Completely online</h4>
            <p className="mb-0 text-muted">
              FileBee is a browser-based tool which means that you don't need to
              download anything to your device because it works online.
            </p>
          </div>
          <div className="col-sm-6 col-md-4 mb-5">
            <div className="my-3">
              <i className="fab fa-2x fa-sass text-primary"></i>
            </div>
            <h4 className="h5 mb-2">How it works</h4>
            <p className="mb-0 text-muted">
              Upload a file from your device. Click "Convert", wait a moment
              while the tool is processing the file and save the result.
            </p>
          </div>
          <div className="col-sm-6 col-md-4 mb-5">
            <div className="my-3">
              <i className="fa fa-2x fa-file-export text-primary"></i>
            </div>
            <h4 className="h5 mb-2">Unlimited file conversions</h4>
            <p className="mb-0 text-muted">
              FileBee supports all sorts of commonly-used mimetypes like PDF,
              JPEG, PNG, MP3 and lot others.
            </p>
          </div>
          <div className="col-sm-6 col-md-4 mb-5">
            <div className="my-3">
              <i className="far fa-2x fa-life-ring text-primary"></i>
            </div>
            <h4 className="h5 mb-2">All platforms supported</h4>
            <p className="mb-0 text-muted">
              All development and production related dependencies can be
              installed through npm and used in any way you like.
            </p>
          </div>
          <div className="col-sm-6 col-md-4 mb-5">
            <div className="my-3">
              <i className="fa fa-2x fa-boxes text-primary"></i>
            </div>
            <h4 className="h5 mb-2">Privacy guaranteed</h4>
            <p className="mb-0 text-muted">
              Don't worry, we delete input files right after editing and output
              files after few hours that is why no one can access them. Read
              more about security.
            </p>
          </div>
          <div className="col-sm-6 col-md-4 mb-5">
            <div className="my-3">
              <i className="fab fa-2x fa-gulp text-primary"></i>
            </div>
            <h4 className="h5 mb-2">Easy to use</h4>
            <p className="mb-0 text-muted">
              The interface is very simple and intuitive, it doesn't require any
              extra actions! It was designed to make it easy for anyone to
              convert files.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Features;
