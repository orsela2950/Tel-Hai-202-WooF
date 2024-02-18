from os.path import join, abspath, dirname

msgs_dir = join(abspath(dirname(__file__)), 'html_messages')
ban_msg_path = join(msgs_dir, 'ban_msg.html')
ban_msg_css_path = join(msgs_dir, 'ban_msg.css')

error_msg_path = join(msgs_dir, 'error_msg.html')
error_msg_css_path = join(msgs_dir, 'error_msg.css')

denial_msg_path = join(msgs_dir, 'denied_msg.html')


def load_ban_message(ip, reason, expiration, source):
    with (open(ban_msg_path, 'r') as ban_msg_html,
          open(ban_msg_css_path, 'r') as ban_msg_css):
        # Insert the params into the HTML template
        return ban_msg_html.read().format(style=ban_msg_css.read(), ip=ip, reason=reason, expiration=expiration, source=source)


def load_error_message(e: Exception):
    with (open(error_msg_path, 'r') as error_msg_html,
          open(error_msg_css_path, 'r') as error_msg_css):
        # Insert the error message into the HTML template
        return error_msg_html.read().format(style=error_msg_css.read(), error=e)


def load_denied_message():
    with open(denial_msg_path, mode='r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    load_ban_message('hello', '','','')
    load_error_message(Exception("hello"))
    print(type(load_denied_message()))
