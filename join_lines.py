import sublime, sublime_plugin

class JoinLinesPrompt(sublime_plugin.WindowCommand):

    def run(self):
        self.window.show_input_panel('Join characters:', '',
                                     self.on_done, None, None)

    def on_done(self, text):
        self.window.active_view().run_command('join_lines_custom',
                                              {'joinstr': text})

class JoinLinesCustom(sublime_plugin.TextCommand):

    def run(self, edit, joinstr):
        for sel in self.view.sel():
            if sel.empty():
                # This line and the next one.
                line_r = self.view.line(sel)
                # print('line_r=(%i, %i)' % (line_r.a, line_r.b))
                # Next line.
                row, col = self.view.rowcol(sel.a)
                # print('row=%i col=%i' % (row, col))
                next_line_p = self.view.text_point(row+1, 0)
                if line_r.contains(next_line_p):
                    # This was the last line in the file.
                    print('exit, no more lines')
                    return
                # print('next_line_point = %i' % next_line_p)
                next_line_r = self.view.line(next_line_p)
                if next_line_r.empty() and next_line_r.a == self.view.size():
                    # Last line is empty, don't join with it.
                    print('last line empty, dont join')
                    return
                # print('next_line_r=(%i, %i)' % (next_line_r.a, next_line_r.b))
                line_rs = [line_r, next_line_r]
            else:
                line_rs = self.view.lines(sel)
            lines = [self.view.substr(r) for r in line_rs]
            full_region = sublime.Region(line_rs[0].begin(), line_rs[-1].end())
            result = joinstr.join(lines)
            self.view.replace(edit, full_region, result)
