from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    post_map = map(lambda post: schemas.PostResponseVotes(**post), res.json()) # In this way I mapped res.json() to schemas I build in main app. Now I can test if response is equal to posts created in 'test_posts', but to make it easier I only tested the length of the output.
    
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/8888888888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostResponseVotes(**res.json())
    # print(post)
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
    assert post.Posts.title == test_posts[0].title
    # assert res.status_code == 404

