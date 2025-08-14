from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from models import Category

class ArticleForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Nội dung', validators=[DataRequired()])
    excerpt = TextAreaField('Tóm tắt', validators=[Length(max=300)])
    category_id = SelectField('Chuyên mục', coerce=int, validators=[DataRequired()])
    featured_image = StringField('Ảnh đại diện (URL)')
    featured = BooleanField('Bài viết nổi bật')
    published = BooleanField('Xuất bản', default=True)
    
    # SEO fields
    meta_title = StringField('Meta Title', validators=[Length(max=200)])
    meta_description = TextAreaField('Meta Description', validators=[Length(max=300)])
    meta_keywords = StringField('Meta Keywords', validators=[Length(max=500)])
    
    submit = SubmitField('Lưu bài viết')
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # Populate category choices
        self.category_id.choices = [(cat.id, cat.name) for cat in Category.query.all()]

class ContactForm(FlaskForm):
    name = StringField('Họ tên', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Chủ đề', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Tin nhắn', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Gửi tin nhắn')

class SearchForm(FlaskForm):
    query = StringField('Tìm kiếm...', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Tìm kiếm')
