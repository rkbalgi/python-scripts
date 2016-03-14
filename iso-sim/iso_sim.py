from spec import Spec
from iso8583_v0 import Iso8583v0Spec
import binascii
import Tkinter as Tk
import ttk
import Tix
from spec_msg_def import SpecMessageDef


def set_components(top):
    spec = Spec.get_spec('Iso8583 v0 - Test')
    top.title = top.title + ' - ' + spec.name
    spec_tree = ttk.Treeview(top, columns=('Field', 'Field Encoding', 'Field Value'), selectmode='browse')
    msg = spec.get_msg_by_name('Authorization Message - 0100')

    for field_def in msg.req_fields:
        print field_def.name
        spec_tree.insert('', 'end', field_def.name, text=field_def.name,
                         values=field_def.name + ',' + field_def.encoding)

    spec_tree.pack()


if __name__ == "__main__":
    Spec.register_spec(Iso8583v0Spec())

    top = Tk.Tk()
    top.title = 'ISO8583 Simulator'
    top.configure(height=600, width=600)
    set_components(top)
    top.mainloop()


    # Spec.register_spec(Iso8583v0Spec())
    # spec = Spec.get_spec('Iso8583 v0 - Test')
    # msg = spec.parse(binascii.unhexlify(
    #    'f1f1f0f0' + 'F3000000200000018000000000000001' + '0F313231313131313131313131313134' + '303034303030' +
    #    '31323334353637383930' + '30333033' + '313130303030' + 'F0F1F5F1F2F1F1F1F1F1F1F1F1F1F1F1F1F4' +
    #    'e3456af57b0198f4' + 'F0F0F4F0F0F0F8' + 'e3456af57b0198f4'))
