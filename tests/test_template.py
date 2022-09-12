import pytest


# To test if an authorized user can get all templates
def test_get_all_templates(client, token):
    res = client.get("/template", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


# To test if an unauthorized user can get all templates
def test_unauthorized_user_get_all_templates(client):
    res = client.get("/template")
    assert res.status_code == 401


# To test if an unauthorized user can get one template
def test_unauthorized_user_get_one_template(client):
    res = client.get(f"/template/19")
    assert res.status_code == 401


# To get a template that does not exist
def test_get_one_template_not_exist(client, token):
    res = client.get("/template/8888", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404


# To test if an authorized user can get one template
def test_get_one_template(client, token):
    res = client.get("/template/19", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200


# Test create template with authorized user
@pytest.mark.parametrize("template_name, subject, body", {
    ("hello", "to the big steppers", "Kendrick"),
    ("jaden", "ninety", "Syre"),
    ("Kendrick", "n95", "Mr Morale")
    })
def test_create_template(client, token, template_name, subject, body):
    res = client.post("/template", json={"template_name": template_name, "subject": subject, "body": body}, headers={"Authorization": f"Bearer {token}"})

    created_template = res.json
    assert res.status_code == 201
    assert created_template["template_name"] == template_name
    assert created_template["subject"] == subject
    assert created_template["body"] == body


# Test if an unauthorized user can create template
def test_unauthorized_user_create_template(client):
    res = client.post("/template", json={"template_name": "template", "subject": "subject", "body": "body"})
    assert res.status_code == 401


# Test if an unauthorized user can delete template
def test_unauthorized_user_delete_template(client):
    res = client.delete(f"/template/20")
    assert res.status_code == 401


# Test if an authorized user can delete template created by them
def test_delete_template_success(client, token):
    res = client.delete(f"/template/23", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 204


# Test to delete a template that does not exist
def test_delete_template_non_exist(client, token):
    res = client.delete("/template/888888", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404


# Test to delete another user's template
def test_delete_other_user_template(client, another_token):
    res = client.delete("/template/14", headers={"Authorization": f"Bearer {another_token}"})
    assert res.status_code == 403


# Test to check if an authorized user can update a template
def test_update_template(client, token):
    data = {
        "template_name": "updated template",
        "body": "updated body",
    }
    res = client.put("template/14", json=data, headers={"Authorization": f"Bearer {token}"})
    updated_template = res.json
    assert res.status_code == 200
    assert updated_template["template_name"] == data["template_name"]
    assert updated_template["body"] == data["body"]


# Test if a user can update another user's template
def test_update_other_user_template(client, another_token):
    data = {
        "template_name": "updated template",
        "body": "updated body",
    }
    res = client.put("template/14", json=data, headers={"Authorization": f"Bearer {another_token}"})
    assert res.status_code == 403


# Test if unauthorized user can update template
def test_unauthorized_update_template(client):
    data = {
        "template_name": "updated template",
        "body": "updated body",
    }
    res = client.put(f"/template/14", json=data)
    assert res.status_code == 401


# Test to update template that does not exist
def test_update_template_does_not_exist(client, token):
    data = {
        "template_name": "updated template",
        "body": "updated body",
    }
    res = client.put(f"/template/8888", json=data, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 404


