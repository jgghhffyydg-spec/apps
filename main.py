import hashlib
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# ===== Node =====
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}

    def store(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return f"Node(ID={self.node_id})"


# ===== DHT =====
class SimpleDHT:
    def __init__(self, nodes):
        self.nodes = sorted(nodes, key=lambda n: n.node_id)

    def hash_key(self, key):
        h = hashlib.sha1(key.encode()).hexdigest()
        return int(h, 16) % 100

    def find_node(self, key_hash):
        for node in self.nodes:
            if node.node_id >= key_hash:
                return node
        return self.nodes[0]

    def store(self, key, value):
        key_hash = self.hash_key(key)
        node = self.find_node(key_hash)
        node.store(key, value)
        return f"📦 تم تخزين '{key}' في {node}"

    def lookup(self, key):
        key_hash = self.hash_key(key)
        node = self.find_node(key_hash)
        value = node.data.get(key, None)
        if value:
            return f"🔍 وُجد في {node}: {value}"
        else:
            return f"❌ '{key}' غير موجود"


# ===== Kivy UI =====
class DHTChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # إنشاء DHT
        nodes = [Node(10), Node(30), Node(50), Node(70)]
        self.dht = SimpleDHT(nodes)

        # شاشة المحادثة
        self.chat_label = Label(
            size_hint_y=None,
            markup=True,
            text="",
            halign="left",
            valign="top"
        )
        self.chat_label.bind(
            width=lambda *x: self.chat_label.setter("text_size")(self.chat_label, (self.chat_label.width, None))
        )

        self.scroll = ScrollView(size_hint=(1, 0.6))
        self.scroll.add_widget(self.chat_label)

        # المدخلات
        self.key_input = TextInput(hint_text="Key (مثال: user1)", size_hint_y=0.1)
        self.value_input = TextInput(hint_text="Message", size_hint_y=0.1)

        # الأزرار
        btn_layout = BoxLayout(size_hint_y=0.1)
        store_btn = Button(text="إرسال / تخزين")
        lookup_btn = Button(text="بحث")

        store_btn.bind(on_press=self.store_data)
        lookup_btn.bind(on_press=self.lookup_data)

        btn_layout.add_widget(store_btn)
        btn_layout.add_widget(lookup_btn)

        # إضافة العناصر
        self.add_widget(self.scroll)
        self.add_widget(self.key_input)
        self.add_widget(self.value_input)
        self.add_widget(btn_layout)

    def store_data(self, instance):
        key = self.key_input.text
        value = self.value_input.text
        if key and value:
            result = self.dht.store(key, value)
            self.chat_label.text += f"\n[color=00ff00]{result}[/color]"
            self.value_input.text = ""

    def lookup_data(self, instance):
        key = self.key_input.text
        if key:
            result = self.dht.lookup(key)
            self.chat_label.text += f"\n[color=ffff00]{result}[/color]"


class DHTChatApp(App):
    def build(self):
        return DHTChatUI()


if __name__ == "__main__":
    DHTChatApp().run()
