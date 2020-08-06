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