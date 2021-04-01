from handlers.uploading import upload_handler


def test_upload_handler():
    # test the upload handler
    a = upload_handler("test.py")

    assert a.status == True