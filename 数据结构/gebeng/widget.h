#ifndef WIDGET_H
#define WIDGET_H


#include<QWidget>
#include<QPainter>
#include<random>
#include<iostream>
using namespace std;
QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = nullptr);
    ~Widget();
    void paintEvent(QPaintEvent *event) override;
private slots:
    void on_adj_matrix_btn_clicked();

    void on_adj_list_btn_clicked();

    void on_min_path_btn_clicked();

private:
    Ui::Widget *ui;

};
#endif // WIDGET_H
