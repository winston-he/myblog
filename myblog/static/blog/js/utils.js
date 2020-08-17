function getBlogPostPreviewItem(blogPostItem) {
    var r = blogPostItem;
    var text = '<li class="list-group-item post-item"></li>'
    var text = r.published_time?'<li class="list-group-item post-item"></li>':'<li class="list-group-item draft-item"></li>';
    text += "<div class=\"preview-post-title\">";
        text += "    <h4><a href=POST_DETAIL_URL_PLACEHOLDER class=\"post-title-link\">".replace("POST_DETAIL_URL_PLACEHOLDER", "{%url 'post_detail' pk=123%}".replace(r.id));
        text += "<span style=\"font-size: 30px;\">POST_TITLE_PLACEHOLDER</span></a></h4>".replace("POST_TITLE_PLACEHOLDER", r.title);
        text += "</div>";
        text += "<div class=\"preview-post-date\">";
        text += "    <p>Created on: POST_CREATE_TIME_PLACEHOLDER".replace("POST_CREATE_TIME_PLACEHOLDER", r.create_time);
        text +=" by: POST_AUTHOR_PLACEHOLDER</p>".replace("POST_AUTHOR_PLACEHOLDER", r.author);
        text += "</div>";
        text += "<div class=\"preview-post-content\">";
        text += "    <p>";
        text += r.content.slice(0, 140)
        text += "    </p>";
        text += "</div>";
        text += "<div class=\"preview-visit-stats\">";
        text += "        <div id=\"liked-count\" class=\"stats\"><img src=\"{%static 'img/icons/red_heart.png'%}\" width=20 height=20 alt=\"\">POST_LIKED_BY_PLACEHOLDER</div>".replace("POST_LIKED_BY_PLACEHOLDER", r.liked_count);
        text += "        <div id=\"marked-count\" class=\"stats\"><img src=\"{%static 'img/icons/star.png'%}\" width=20 height=20 alt=\"\">POST_MARKED_BY_PLACEHOLDER</div>".replace("POST_MARKED_BY_PLACEHOLDER", r.marked_count);
        text += "        <div id=\"viewed-count\" class=\"stats\"><img src=\"{%static 'img/icons/view.png'%}\" width=20 height=20 alt=\"\"> POST_VIEW_COUNT_PLACEHOLDER</div>".replace("POST_VIEW_COUNT_PLACEHOLDER", r.viewed_count);
        text += "        <div id=\"comment-count\" class=\"stats\"><img src=\"{%static 'img/icons/comment.png'%}\" width=20 height=20 alt=\"\">POST_COMMENT_COUNT_PLACEHOLDER</div>".replace("POST_COMMENT_COUNT_PLACEHOLDER", r.comment_count);
        text += "</div>";
        text += "</li>";
    return text
}

function getPostCommentItem(data) {
    var text = "";
    text += "<div class=\"comment-item\" id=\"comment-item_PK_PLACEHOLDER\">".replace("PK_PLACEHOLDER", data.pk);
    text += "  <div class=\"card-header comment-header\">";
    text += "    <div class=\"d-flex w-100 justify-content-between\">";
    text += "      Posted by: me";
    text += "    </div>";
    text += "  </div>";
    text += "    <h6 class=comment-title\">";
    text += "      <small>{{comment.create_time | date:\"N d, Y P\"}}</small>";
    text += "    </h6>";
    text += "    <p class=\"comment-text\"><p class=\"mb-1\">" + data.content +"</p>";
    text += "    <div class=\"comment-actions\">";
    text += "        <div class=\"comment-action-item like-comment\">";
    text += "          <a role=\"button\">";
    text += "              <img data-href=\"{% url 'like_comment' pk=123 %}\" src=\"{%static 'img/icons/thumb_up_unselected.png'%}\" class=\"like-comment\" id=\"like-".replace("123", data.pk) + data.pk + "\" width=20 height=20>";
    text += "          </a>";
    text += "          <div id=\"comment-like-number_" + data.pk + "\" class=comment-action-item>" + data.likes_count + "</div>";
    text += "        </div>";
    text += "        ";
    text += "        <div class=\"comment-action-item dislike-comment\">";
    text += "          <a role=\"button\">";
    text += "              <img data-href=\"{% url 'dislike_comment' 123 %}\" src=\"{%static 'img/icons/thumb_down_unselected.png'%}\" class=\"dislike-comment\" id=\"dislike-123\" width=20 height=20>".replace("123", data.pk);
    text += "          </a>";
    text += "          <div id=\"comment-dislike-number_" + data.pk + "\" class=comment-action-item>"  + data.dislikes_count + "</div>";
    text += "        </div>";
    text += "        <div class=\"comment-action-item remove-comment\">";
    text += "          <button type=\"button\" data-href=\"{%url 'comment_remove' pk=123%}\" class=\"delete-comment-btn\" id=\"delete_123\" id=PK_><img src=\"{%static 'img/icons/trash_bin.png'%}\" width=20 height=20></button>".replace("123", data.pk);
    text += "        </div>";
    text += "    </div>";
    text += "</div>";
}