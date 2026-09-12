from micropython import const
import framebuf


_SET_CONTRAST = const(0x81)
_SET_ENTIRE_ON = const(0xA4)
_SET_NORM_INV = const(0xA6)
_SET_DISP = const(0xAE)
_SET_MEM_ADDR = const(0x20)
_SET_COL_ADDR = const(0x21)
_SET_PAGE_ADDR = const(0x22)
_SET_DISP_START_LINE = const(0x40)
_SET_SEG_REMAP = const(0xA0)
_SET_MUX_RATIO = const(0xA8)
_SET_COM_OUT_DIR = const(0xC0)
_SET_DISP_OFFSET = const(0xD3)
_SET_COM_PIN_CFG = const(0xDA)
_SET_DISP_CLK_DIV = const(0xD5)
_SET_PRECHARGE = const(0xD9)
_SET_VCOM_DESEL = const(0xDB)
_SET_CHARGE_PUMP = const(0x8D)


class SH1106:
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc

        self.pages = self.height // 8

        self.buffer = bytearray(
            self.pages * self.width
        )

        self.framebuf = framebuf.FrameBuffer(
            self.buffer,
            self.width,
            self.height,
            framebuf.MONO_VLSB,
        )

        self.poweron()
        self.init_display()

    def init_display(self):
        for command in (
            _SET_DISP | 0x00,
            _SET_DISP_CLK_DIV,
            0x80,
            _SET_MUX_RATIO,
            self.height - 1,
            _SET_DISP_OFFSET,
            0x00,
            _SET_DISP_START_LINE | 0x00,
            _SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            _SET_MEM_ADDR,
            0x00,
            _SET_SEG_REMAP | 0x01,
            _SET_COM_OUT_DIR | 0x08,
            _SET_COM_PIN_CFG,
            0x12 if self.height == 64 else 0x02,
            _SET_CONTRAST,
            0x9F,
            _SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            _SET_VCOM_DESEL,
            0x40,
            _SET_ENTIRE_ON,
            _SET_NORM_INV,
            _SET_DISP | 0x01,
        ):
            self.write_cmd(command)

        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(
            _SET_DISP | 0x00
        )

    def poweron(self):
        self.write_cmd(
            _SET_DISP | 0x01
        )

    def contrast(self, contrast):
        self.write_cmd(
            _SET_CONTRAST
        )

        self.write_cmd(
            contrast
        )

    def invert(self, invert):
        self.write_cmd(
            _SET_NORM_INV | (invert & 1)
        )

    def show(self):
        for page in range(self.pages):
            self.write_cmd(
                0xB0 + page
            )

            self.write_cmd(
                0x02
            )

            self.write_cmd(
                0x10
            )

            start = (
                self.width * page
            )

            end = start + self.width

            self.write_data(
                self.buffer[start:end]
            )

    def fill(self, color):
        self.framebuf.fill(
            color
        )

    def pixel(self, x, y, color=None):
        if color is None:
            return self.framebuf.pixel(
                x,
                y,
            )

        self.framebuf.pixel(
            x,
            y,
            color,
        )

    def hline(self, x, y, width, color):
        self.framebuf.hline(
            x,
            y,
            width,
            color,
        )

    def vline(self, x, y, height, color):
        self.framebuf.vline(
            x,
            y,
            height,
            color,
        )

    def line(self, x1, y1, x2, y2, color):
        self.framebuf.line(
            x1,
            y1,
            x2,
            y2,
            color,
        )

    def rect(self, x, y, width, height, color):
        self.framebuf.rect(
            x,
            y,
            width,
            height,
            color,
        )

    def fill_rect(
        self,
        x,
        y,
        width,
        height,
        color,
    ):
        self.framebuf.fill_rect(
            x,
            y,
            width,
            height,
            color,
        )

    def text(
        self,
        text,
        x,
        y,
        color=1,
    ):
        self.framebuf.text(
            text,
            x,
            y,
            color,
        )


class SH1106_I2C(SH1106):
    def __init__(
        self,
        width,
        height,
        i2c,
        addr=0x3C,
        external_vcc=False,
    ):
        self.i2c = i2c
        self.addr = addr

        self.temp = bytearray(2)

        super().__init__(
            width,
            height,
            external_vcc,
        )

    def write_cmd(self, command):
        self.temp[0] = 0x80
        self.temp[1] = command

        self.i2c.writeto(
            self.addr,
            self.temp,
        )

    def write_data(self, buffer):
        self.i2c.writevto(
            self.addr,
            (
                b"\x40",
                buffer,
            ),
        )